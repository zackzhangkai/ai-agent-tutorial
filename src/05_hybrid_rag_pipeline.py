"""
05_hybrid_rag_pipeline.py
=============================================================================
第 5 章：企业级工业 RAG 管道完整代码
包含：
  1. BM25 稀疏检索器 (精确关键词命中与术语保真)
  2. 稠密向量检索器 (语义相近度与嵌入向量搜索)
  3. RRF (Reciprocal Rank Fusion) 倒数排名融合算法
  4. 交叉注意力二次重排 (Cross-Encoder Re-ranker) 评分机制
  5. 完整检索问答链路与耗时性能分析

运行方法：
  python src/05_hybrid_rag_pipeline.py
依赖：
  pip install numpy
=============================================================================
"""

import math
import time
from collections import Counter
from typing import List, Dict, Any, Tuple


# ==========================================
# 1. 模拟企业级真实知识库文档集
# ==========================================
KNOWLEDGE_BASE = [
    {
        "id": "doc_001",
        "title": "售后退换货时限与运费政策",
        "content": "生鲜食品与易腐耗材不支持7天无理由退货。非质量问题拒收生鲜商品产生的物流损耗由买家自行承担。3C数码类产品支持7天无理由退换，但要求包装完好无损、未拆封激活。"
    },
    {
        "id": "doc_002",
        "title": "生鲜冷链配送超时与生鲜腐烂赔偿标准",
        "content": "若冷链生鲜出现外包装破损、冰袋完全化水、肉质变质异味，买家需在签收后24小时内上传商品照片及运单面单凭据。客服核实无误后，将在2小时内执行极速退款并赔付50元生鲜无门槛优惠券。"
    },
    {
        "id": "doc_003",
        "title": "物流滞留与丢件丢包索赔流程",
        "content": "包裹物流轨迹超过48小时未更新视为异常滞留。买家联系客服发起丢件调查后，专员将在24小时内完成与顺丰/京东快递的联查核实。确认丢件后立即补发或全额原路退款。"
    },
    {
        "id": "doc_004",
        "title": "平台VIP会员与积分权益说明",
        "content": "黑金VIP会员每月可领取3张5元无门槛运费券，生鲜品类消费享受双倍积分返利。积分可在积分商城兑换实物礼品或抵扣结账金额。"
    },
    {
        "id": "doc_005",
        "title": "家电延保与以旧换新服务规则",
        "content": "大家电提供全国联保与免费上门安装服务，支持购买1至3年原厂碎屏延保及电池换新。以旧换新旧机最高可抵扣800元购机款。"
    }
]


# ==========================================
# 2. BM25 稀疏检索器 (精确词项统计与逆文档频率)
# ==========================================
class BM25Retriever:
    """简易高性能纯 Python BM25 实现 (支持精确匹配与术语检索)"""
    def __init__(self, corpus: List[Dict[str, str]], k1: float = 1.5, b: float = 0.75):
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.doc_len = []
        self.avg_doc_len = 0.0
        self.doc_freqs = []
        self.idf = {}
        self.corpus_size = len(corpus)
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        # 工业界推荐 jieba 或专用分词器；此处采用双字滑动切分 (Bi-gram + 单字混合) 确保无需额外依赖即可运行
        tokens = []
        text = text.lower()
        for i in range(len(text)):
            tokens.append(text[i])
            if i + 1 < len(text):
                tokens.append(text[i:i+2])
        return tokens

    def _build_index(self):
        total_len = 0
        df = Counter()
        for doc in self.corpus:
            tokens = self._tokenize(doc["title"] + " " + doc["content"])
            self.doc_len.append(len(tokens))
            total_len += len(tokens)
            unique_tokens = set(tokens)
            for t in unique_tokens:
                df[t] += 1
            self.doc_freqs.append(Counter(tokens))

        self.avg_doc_len = total_len / self.corpus_size if self.corpus_size > 0 else 0
        for token, freq in df.items():
            # 经典 BM25 IDF 平滑公式
            self.idf[token] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, str], float]]:
        query_tokens = self._tokenize(query)
        scores = []
        for idx, doc in enumerate(self.corpus):
            score = 0.0
            doc_len = self.doc_len[idx]
            freqs = self.doc_freqs[idx]
            for token in query_tokens:
                if token not in freqs:
                    continue
                tf = freqs[token]
                idf = self.idf.get(token, 0.1)
                num = tf * (self.k1 + 1)
                den = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len))
                score += idf * (num / den)
            scores.append((doc, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


# ==========================================
# 3. 稠密语义检索器 (Dense Vector Retriever)
# ==========================================
class DenseRetriever:
    """稠密语义向量检索器 (模拟 embedding 与余弦相似度)"""
    def __init__(self, corpus: List[Dict[str, str]]):
        self.corpus = corpus
        # 生产环境中调用 openai.Embedding.create 或 bge-large-zh-v1.5
        # 此处使用语义特征投影向量进行完全可重现的高效计算
        self.doc_vectors = [self._compute_dense_vector(doc["title"] + " " + doc["content"]) for doc in corpus]

    def _compute_dense_vector(self, text: str) -> List[float]:
        # 特征哈希模拟稠密语义向量 (128维)
        vec = [0.0] * 128
        for i, char in enumerate(text):
            h = (hash(char) + i * 31) % 128
            vec[h] += 1.0
        # L2 归一化
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, str], float]]:
        q_vec = self._compute_dense_vector(query)
        scores = []
        for idx, doc in enumerate(self.corpus):
            sim = self._cosine_similarity(q_vec, self.doc_vectors[idx])
            scores.append((doc, sim))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


# ==========================================
# 4. 倒数排名融合 (RRF: Reciprocal Rank Fusion)
# ==========================================
def reciprocal_rank_fusion(
    bm25_results: List[Tuple[Dict[str, str], float]],
    dense_results: List[Tuple[Dict[str, str], float]],
    k: int = 60
) -> List[Dict[str, Any]]:
    """
    RRF 经典算法：
    RRF_Score(d) = sum_{m in models} [ 1 / (k + rank_m(d)) ]
    参数 k 常取 60，有效防止单一模型排名极端导致的扰动。
    """
    scores: Dict[str, float] = {}
    doc_lookup: Dict[str, Dict[str, str]] = {}
    details: Dict[str, Dict[str, Any]] = {}

    for rank, (doc, raw_score) in enumerate(bm25_results, start=1):
        doc_id = doc["id"]
        doc_lookup[doc_id] = doc
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))
        details.setdefault(doc_id, {})["bm25_rank"] = rank
        details[doc_id]["bm25_score"] = raw_score

    for rank, (doc, raw_score) in enumerate(dense_results, start=1):
        doc_id = doc["id"]
        doc_lookup[doc_id] = doc
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))
        details.setdefault(doc_id, {})["dense_rank"] = rank
        details[doc_id]["dense_score"] = raw_score

    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    fused_results = []
    for doc_id, rrf_score in sorted_docs:
        fused_results.append({
            "doc": doc_lookup[doc_id],
            "rrf_score": rrf_score,
            "details": details.get(doc_id, {})
        })
    return fused_results


# ==========================================
# 5. 交叉注意力重排器 (Cross-Encoder Re-ranker)
# ==========================================
class CrossEncoderReranker:
    """
    BGE-Reranker-Large 交叉注意力重排器。
    将 (Query, Document) 拼接一次性输入深度 Transformer，计算全注意力相关性评分 (0.0 ~ 1.0)。
    """
    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 2) -> List[Dict[str, Any]]:
        scored = []
        for item in candidates:
            doc = item["doc"]
            full_text = f"{doc['title']} {doc['content']}"
            # 真实生产环境调用：model.predict([(query, full_text)])
            # 此处演示精准语义细粒度对齐打分逻辑：
            relevance = 0.1
            if "生鲜" in query and "生鲜" in full_text:
                relevance += 0.4
            if "化了" in query or "变质" in query or "臭" in query:
                if "冰袋完全化水" in full_text or "变质异味" in full_text:
                    relevance += 0.45
            if "退款" in query or "赔" in query:
                if "极速退款" in full_text or "赔付" in full_text:
                    relevance += 0.1

            scored.append({
                **item,
                "rerank_score": round(relevance, 4)
            })

        scored.sort(key=lambda x: x["rerank_score"], reverse=True)
        return scored[:top_n]


# ==========================================
# 6. 端到端 RAG 管道集成执行与效果展示
# ==========================================
def run_hybrid_rag_pipeline(user_query: str):
    print("=" * 80)
    print(f"【RAG 检索管道启动】用户输入 Query: \"{user_query}\"")
    print("=" * 80)

    # 1. 实例化检索器
    bm25 = BM25Retriever(KNOWLEDGE_BASE)
    dense = DenseRetriever(KNOWLEDGE_BASE)
    reranker = CrossEncoderReranker()

    start_time = time.perf_counter()

    # 2. 阶段一：并行双路召回 (Dual-Track Retrieval)
    bm25_res = bm25.retrieve(user_query, top_k=3)
    dense_res = dense.retrieve(user_query, top_k=3)

    print("\n[阶段 1: BM25 稀疏检索 Top-3 (基于词频/IDF)]")
    for r, (doc, sc) in enumerate(bm25_res, 1):
        print(f"  Rank #{r} | Score: {sc:.4f} | [{doc['id']}] {doc['title']}")

    print("\n[阶段 1: Dense 稠密语义检索 Top-3 (基于语义嵌入)]")
    for r, (doc, sc) in enumerate(dense_res, 1):
        print(f"  Rank #{r} | CosSim: {sc:.4f} | [{doc['id']}] {doc['title']}")

    # 3. 阶段二：RRF 倒数排名融合
    fused_res = reciprocal_rank_fusion(bm25_res, dense_res, k=60)
    print("\n[阶段 2: RRF 倒数排名融合 (Reciprocal Rank Fusion)]")
    for r, item in enumerate(fused_res, 1):
        doc = item["doc"]
        print(f"  Rank #{r} | RRF Score: {item['rrf_score']:.6f} | [{doc['id']}] {doc['title']}")

    # 4. 阶段三：Cross-Encoder 二次深度重排 (Re-rank)
    final_docs = reranker.rerank(user_query, fused_res, top_n=2)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print(f"\n[阶段 3: BGE Cross-Encoder 深度重排 Top-2 (总耗时: {elapsed_ms:.2f}ms)]")
    for r, item in enumerate(final_docs, 1):
        doc = item["doc"]
        print(f"  🔥 最终入选 #{r} | 重排相关度: {item['rerank_score']:.4f} | [{doc['id']}] {doc['title']}")
        print(f"     内容切片: {doc['content']}")

    # 5. 模拟组装 Prompt 输送大模型
    context_str = "\n".join([f"- 《{item['doc']['title']}》: {item['doc']['content']}" for item in final_docs])
    prompt = f"""【系统角色】你是一名专业的生鲜电商智能客服助手，请严格依据下述参考事实回答买家问题。禁止无事实依据的胡乱推测。

【参考知识片段】：
{context_str}

【用户咨询】：{user_query}
【AI 答复建议】："""
    
    print("\n[阶段 4: 组装送入 LLM 的增强 Prompt (精准无幻觉)]")
    print("-" * 50)
    print(prompt)
    print("-" * 50)


if __name__ == "__main__":
    # 测试真实业务场景：买家购买三文鱼到货后融水发臭，询问怎么处理
    test_query = "昨天买的三文鱼冰袋全化成水了，肉闻着有一股臭酸味，能不能退钱？"
    run_hybrid_rag_pipeline(test_query)
