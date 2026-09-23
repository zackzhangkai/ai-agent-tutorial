import Foundation
import Vision
import AppKit

func codes(_ path: String) throws -> Set<String> {
    let request = VNDetectBarcodesRequest()
    request.symbologies = [.qr]
    try VNImageRequestHandler(url: URL(fileURLWithPath: path), options: [:]).perform([request])
    return Set((request.results ?? []).compactMap { $0.payloadStringValue })
}

let paths = Array(CommandLine.arguments.dropFirst())
guard paths.count >= 2 else { fatalError("Provide two source images and optional poster paths") }
let personal = try codes(paths[0])
let group = try codes(paths[1])
print("Source personal QR decoded: \(personal.count)")
print("Source group QR decoded: \(group.count)")
for path in paths.dropFirst(2) {
    let found = try codes(path)
    print("\(URL(fileURLWithPath: path).lastPathComponent): decoded=\(found.count), personalMatches=\(!personal.isEmpty && personal.isSubset(of: found)), groupMatches=\(!group.isEmpty && group.isSubset(of: found))")
}
