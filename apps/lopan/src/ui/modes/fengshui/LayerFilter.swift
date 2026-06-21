// ContentView.swift
// 風水羅盤ワークステーション — Fortune Workstation
// SwiftUI / 標準ライブラリのみ / ダークモード対応

import SwiftUI

// MARK: - データモデル

enum LuopanPurpose: String, CaseIterable {
    case geLong   = "格龍"
    case liXiang  = "立向"
    case shouShui = "収水"

    var color: Color {
        switch self {
        case .geLong:   return Color(red: 0.55, green: 0.85, blue: 0.60) // 青緑
        case .liXiang:  return Color(red: 0.95, green: 0.80, blue: 0.40) // 金
        case .shouShui: return Color(red: 0.45, green: 0.75, blue: 0.95) // 水色
        }
    }

    var icon: String {
        switch self {
        case .geLong:   return "mountain.2.fill"
        case .liXiang:  return "location.north.fill"
        case .shouShui: return "drop.fill"
        }
    }
}

enum RingSystem: String {
    case sanHe   = "三合"
    case sanYuan = "三元"
    case mixed   = "兼用"
    case special = "特殊"
}

struct LuopanLayer: Identifiable {
    let id: Int
    let name: String
    let ring: RingSystem
    let purposes: Set<LuopanPurpose>
    let isPrecise: Bool   // 104分割層かどうか
    let notes: String
}

// 十二支
struct Shizhi: Identifiable {
    let id: Int            // 0=子 〜 11=亥
    let name: String
    let startHour: Int     // 開始時刻（24h）
    let primaryPurpose: LuopanPurpose
    let recommendedPurposes: Set<LuopanPurpose>

    var timeRange: String {
        let end = (startHour + 2) % 24
        return String(format: "%02d:00〜%02d:00", startHour, end)
    }
}

// MARK: - マスターデータ

extension LuopanLayer {
    static let allLayers: [LuopanLayer] = [
        LuopanLayer(id:  1, name: "天池（磁針穴）",  ring: .mixed,   purposes: [],                        isPrecise: false, notes: "中心穴"),
        LuopanLayer(id:  2, name: "先天八卦",        ring: .mixed,   purposes: [.geLong],                 isPrecise: false, notes: "来龍五行補正"),
        LuopanLayer(id:  3, name: "後天八卦",        ring: .mixed,   purposes: [.liXiang, .shouShui],     isPrecise: false, notes: "向首・水口基準"),
        LuopanLayer(id:  4, name: "九星（洛書）",    ring: .sanYuan, purposes: [.liXiang],                isPrecise: false, notes: "飛星盤基底"),
        LuopanLayer(id:  5, name: "五行（三合）",    ring: .sanHe,   purposes: [.geLong, .shouShui],      isPrecise: false, notes: "龍・水五行"),
        LuopanLayer(id:  6, name: "纳甲",            ring: .mixed,   purposes: [.geLong],                 isPrecise: false, notes: "干支配当"),
        LuopanLayer(id:  7, name: "天干（十干）",    ring: .mixed,   purposes: [.liXiang, .geLong],       isPrecise: false, notes: "方位配置"),
        LuopanLayer(id:  8, name: "穿山七十二龍",   ring: .sanHe,   purposes: [.geLong],                 isPrecise: false, notes: "来龍格定核心"),
        LuopanLayer(id:  9, name: "透地六十龍",     ring: .sanHe,   purposes: [.geLong],                 isPrecise: false, notes: "地中龍脈"),
        LuopanLayer(id: 10, name: "地盤正針",        ring: .sanHe,   purposes: [.geLong, .liXiang],       isPrecise: false, notes: "三合派主盤"),
        LuopanLayer(id: 11, name: "人盤中針",        ring: .sanHe,   purposes: [.liXiang],                isPrecise: false, notes: "7.5°偏移"),
        LuopanLayer(id: 12, name: "天盤縫針",        ring: .sanHe,   purposes: [.shouShui],               isPrecise: false, notes: "15°偏移"),
        LuopanLayer(id: 13, name: "分金（120分）",  ring: .sanHe,   purposes: [.geLong, .liXiang],       isPrecise: false, notes: "3°単位微調整"),
        LuopanLayer(id: 14, name: "正針二十四山",   ring: .sanYuan, purposes: [.liXiang, .geLong],       isPrecise: true,  notes: "玄空飛星坐向基準"),
        LuopanLayer(id: 15, name: "玄空六十四卦",   ring: .sanYuan, purposes: [.liXiang, .shouShui],     isPrecise: true,  notes: "向首・来水卦位"),
        LuopanLayer(id: 16, name: "七十二穿山虎",   ring: .sanYuan, purposes: [.geLong],                 isPrecise: true,  notes: "三元龍格定"),
        LuopanLayer(id: 17, name: "百二十分金",     ring: .sanYuan, purposes: [.liXiang],                isPrecise: true,  notes: "三元精密分金"),
        LuopanLayer(id: 18, name: "三元九運",        ring: .sanYuan, purposes: [.liXiang, .shouShui],     isPrecise: true,  notes: "元運判定補助"),
        LuopanLayer(id: 19, name: "天星水法",        ring: .sanHe,   purposes: [.shouShui],               isPrecise: true,  notes: "来水吉凶判定"),
        LuopanLayer(id: 20, name: "黄泉八殺",        ring: .mixed,   purposes: [.shouShui, .liXiang],     isPrecise: true,  notes: "大凶水口回避"),
        LuopanLayer(id: 21, name: "八路四路",        ring: .mixed,   purposes: [.shouShui],               isPrecise: false, notes: "水路吉凶補助"),
        LuopanLayer(id: 22, name: "消水二十四山",   ring: .sanHe,   purposes: [.shouShui],               isPrecise: false, notes: "水口消納"),
        LuopanLayer(id: 23, name: "消砂二十四山",   ring: .sanHe,   purposes: [.liXiang],                isPrecise: false, notes: "砂吉凶判定"),
        LuopanLayer(id: 24, name: "人盤消砂",        ring: .sanHe,   purposes: [.liXiang],                isPrecise: false, notes: "中針砂法補正"),
        LuopanLayer(id: 25, name: "斗首六甲",        ring: .special, purposes: [.geLong, .liXiang],       isPrecise: false, notes: "斗首法補正"),
        LuopanLayer(id: 26, name: "星曜（紫白）",   ring: .sanYuan, purposes: [.liXiang, .shouShui],     isPrecise: false, notes: "飛星盤連動"),
        LuopanLayer(id: 27, name: "奇門遁甲方位",   ring: .special, purposes: [.liXiang, .shouShui],     isPrecise: true,  notes: "時間軸方位"),
    ]

    // L14〜L27（デバッグパネル表示対象）
    static let preciseRange: [LuopanLayer] = allLayers.filter { $0.id >= 14 }
}

extension Shizhi {
    static let all: [Shizhi] = [
        Shizhi(id:  0, name: "子", startHour: 23, primaryPurpose: .liXiang,  recommendedPurposes: [.liXiang, .geLong]),
        Shizhi(id:  1, name: "丑", startHour:  1, primaryPurpose: .shouShui, recommendedPurposes: [.shouShui, .liXiang]),
        Shizhi(id:  2, name: "寅", startHour:  3, primaryPurpose: .geLong,   recommendedPurposes: [.geLong, .liXiang]),
        Shizhi(id:  3, name: "卯", startHour:  5, primaryPurpose: .liXiang,  recommendedPurposes: [.liXiang, .geLong]),
        Shizhi(id:  4, name: "辰", startHour:  7, primaryPurpose: .shouShui, recommendedPurposes: [.shouShui, .liXiang]),
        Shizhi(id:  5, name: "巳", startHour:  9, primaryPurpose: .geLong,   recommendedPurposes: [.geLong, .liXiang]),
        Shizhi(id:  6, name: "午", startHour: 11, primaryPurpose: .liXiang,  recommendedPurposes: [.liXiang, .geLong]),
        Shizhi(id:  7, name: "未", startHour: 13, primaryPurpose: .shouShui, recommendedPurposes: [.shouShui, .liXiang]),
        Shizhi(id:  8, name: "申", startHour: 15, primaryPurpose: .geLong,   recommendedPurposes: [.geLong, .liXiang]),
        Shizhi(id:  9, name: "酉", startHour: 17, primaryPurpose: .liXiang,  recommendedPurposes: [.liXiang, .geLong]),
        Shizhi(id: 10, name: "戌", startHour: 19, primaryPurpose: .shouShui, recommendedPurposes: [.shouShui, .liXiang]),
        Shizhi(id: 11, name: "亥", startHour: 21, primaryPurpose: .geLong,   recommendedPurposes: [.geLong, .liXiang]),
    ]

    static func current() -> Shizhi {
        let h = Calendar.current.component(.hour, from: Date())
        let m = Calendar.current.component(.minute, from: Date())
        let total = h * 60 + m
        if total >= 23 * 60 || total < 1 * 60 { return all[0] }  // 子
        for i in stride(from: 10, through: 1, by: -1) {
            if total >= all[i].startHour * 60 { return all[i] }
        }
        return all[0]
    }
}

// MARK: - ViewModel

@MainActor
final class LuopanViewModel: ObservableObject {

    @Published var currentShizhi: Shizhi = Shizhi.current()
    @Published var isAutoMode: Bool = true
    @Published var showShizhiPicker: Bool = false
    @Published var compassRotation: Double = 0
    @Published var isAnimating: Bool = false

    private var timer: Timer?

    init() { startAutoTimer() }

    // 有効な推奨用途
    var activePurposes: Set<LuopanPurpose> { currentShizhi.recommendedPurposes }

    // L14〜L27 のフィルタ済みリスト
    var filteredPreciseLayers: [LuopanLayer] {
        LuopanLayer.preciseRange.filter { layer in
            !layer.purposes.isDisjoint(with: activePurposes)
        }
    }

    // L14〜L27 の全リスト（フィルタ状態付き）
    var allPreciseLayersWithState: [(layer: LuopanLayer, isActive: Bool)] {
        LuopanLayer.preciseRange.map { layer in
            (layer: layer, isActive: !layer.purposes.isDisjoint(with: activePurposes))
        }
    }

    func selectShizhi(_ shizhi: Shizhi) {
        currentShizhi = shizhi
        isAutoMode = false
        stopAutoTimer()
        animateCompass()
    }

    func enableAutoMode() {
        isAutoMode = true
        currentShizhi = Shizhi.current()
        startAutoTimer()
        animateCompass()
    }

    private func startAutoTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 60, repeats: true) { [weak self] _ in
            Task { @MainActor [weak self] in
                guard let self, self.isAutoMode else { return }
                let newShizhi = Shizhi.current()
                if newShizhi.id != self.currentShizhi.id {
                    withAnimation(.easeInOut(duration: 0.5)) {
                        self.currentShizhi = newShizhi
                    }
                }
            }
        }
    }

    private func stopAutoTimer() { timer?.invalidate(); timer = nil }

    func animateCompass() {
        withAnimation(.easeInOut(duration: 1.2)) {
            compassRotation += Double.random(in: 340...380)
        }
    }

    deinit { timer?.invalidate() }
}

// MARK: - メインView

struct ContentView: View {

    @StateObject private var vm = LuopanViewModel()
    @Environment(\.colorScheme) var colorScheme

    // 背景グラデーション
    private var bgGradient: LinearGradient {
        LinearGradient(
            colors: [
                Color(red: 0.06, green: 0.06, blue: 0.10),
                Color(red: 0.03, green: 0.08, blue: 0.12),
            ],
            startPoint: .top, endPoint: .bottom
        )
    }

    var body: some View {
        ZStack {
            bgGradient.ignoresSafeArea()

            // 背景装飾：微細な同心円
            BackgroundRingsView()

            ScrollView(showsIndicators: false) {
                VStack(spacing: 0) {
                    headerView
                        .padding(.top, 16)
                    compassSection
                        .padding(.top, 8)
                    shizhiSection
                        .padding(.top, 20)
                    debugPanel
                        .padding(.top, 16)
                        .padding(.bottom, 32)
                }
                .padding(.horizontal, 16)
            }
        }
        .preferredColorScheme(.dark)
        .sheet(isPresented: $vm.showShizhiPicker) {
            ShizhiPickerSheet(vm: vm)
        }
    }

    // MARK: ヘッダー
    private var headerView: some View {
        HStack(alignment: .center) {
            VStack(alignment: .leading, spacing: 2) {
                Text("羅盤")
                    .font(.system(size: 28, weight: .thin, design: .serif))
                    .foregroundStyle(.white)
                Text("Fortune Workstation")
                    .font(.system(size: 11, weight: .medium, design: .monospaced))
                    .foregroundStyle(.white.opacity(0.4))
                    .tracking(2)
            }
            Spacer()
            // 現在時刻バッジ
            VStack(alignment: .trailing, spacing: 2) {
                Text(Date(), format: .dateTime.hour().minute())
                    .font(.system(size: 20, weight: .ultraLight, design: .monospaced))
                    .foregroundStyle(.white.opacity(0.9))
                Text(Date(), format: .dateTime.month().day().weekday())
                    .font(.system(size: 10, weight: .regular))
                    .foregroundStyle(.white.opacity(0.4))
            }
        }
        .padding(.horizontal, 4)
    }

    // MARK: 羅盤セクション
    private var compassSection: some View {
        ZStack {
            // 外枠カード
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .fill(Color.white.opacity(0.04))
                .overlay(
                    RoundedRectangle(cornerRadius: 24, style: .continuous)
                        .stroke(Color.white.opacity(0.08), lineWidth: 1)
                )

            VStack(spacing: 16) {
                // 羅盤プレースホルダー
                LuopanCompassView(rotation: vm.compassRotation, shizhi: vm.currentShizhi)
                    .frame(height: 280)

                // 目的ラベル
                HStack(spacing: 12) {
                    ForEach(LuopanPurpose.allCases, id: \.self) { purpose in
                        let isActive = vm.activePurposes.contains(purpose)
                        PurposeBadge(purpose: purpose, isActive: isActive)
                    }
                }
                .padding(.bottom, 4)
            }
            .padding(20)
        }
    }

    // MARK: 時支セクション
    private var shizhiSection: some View {
        VStack(spacing: 10) {
            // 現在の時支カード
            HStack(spacing: 14) {
                // 時支文字
                ZStack {
                    Circle()
                        .fill(vm.currentShizhi.primaryPurpose.color.opacity(0.15))
                        .frame(width: 56, height: 56)
                    Circle()
                        .stroke(vm.currentShizhi.primaryPurpose.color.opacity(0.4), lineWidth: 1)
                        .frame(width: 56, height: 56)
                    Text(vm.currentShizhi.name)
                        .font(.system(size: 26, weight: .thin, design: .serif))
                        .foregroundStyle(vm.currentShizhi.primaryPurpose.color)
                }

                VStack(alignment: .leading, spacing: 4) {
                    HStack(spacing: 6) {
                        Text("現在の時支")
                            .font(.system(size: 11, weight: .medium))
                            .foregroundStyle(.white.opacity(0.4))
                            .tracking(1)
                        if vm.isAutoMode {
                            Label("自動", systemImage: "clock.arrow.circlepath")
                                .font(.system(size: 10, weight: .medium))
                                .foregroundStyle(.green.opacity(0.8))
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(Color.green.opacity(0.12))
                                .clipShape(Capsule())
                        }
                    }
                    Text("\(vm.currentShizhi.name)時  \(vm.currentShizhi.timeRange)")
                        .font(.system(size: 16, weight: .light, design: .monospaced))
                        .foregroundStyle(.white.opacity(0.9))
                    Text("主用途：\(vm.currentShizhi.primaryPurpose.rawValue)")
                        .font(.system(size: 12, weight: .regular))
                        .foregroundStyle(vm.currentShizhi.primaryPurpose.color.opacity(0.9))
                }

                Spacer()

                // 操作ボタン群
                VStack(spacing: 8) {
                    Button {
                        vm.enableAutoMode()
                    } label: {
                        Image(systemName: "clock.arrow.circlepath")
                            .font(.system(size: 16))
                            .foregroundStyle(vm.isAutoMode ? .green : .white.opacity(0.4))
                            .frame(width: 36, height: 36)
                            .background(Color.white.opacity(vm.isAutoMode ? 0.08 : 0.04))
                            .clipShape(Circle())
                    }

                    Button {
                        vm.showShizhiPicker = true
                    } label: {
                        Image(systemName: "hand.tap.fill")
                            .font(.system(size: 14))
                            .foregroundStyle(.white.opacity(0.7))
                            .frame(width: 36, height: 36)
                            .background(Color.white.opacity(0.04))
                            .clipShape(Circle())
                    }
                }
            }
            .padding(16)
            .background(
                RoundedRectangle(cornerRadius: 16, style: .continuous)
                    .fill(Color.white.opacity(0.05))
                    .overlay(
                        RoundedRectangle(cornerRadius: 16, style: .continuous)
                            .stroke(vm.currentShizhi.primaryPurpose.color.opacity(0.25), lineWidth: 1)
                    )
            )

            // 十二支クイック選択（横スクロール）
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    ForEach(Shizhi.all) { shizhi in
                        ShizhiChip(
                            shizhi: shizhi,
                            isSelected: vm.currentShizhi.id == shizhi.id
                        ) {
                            withAnimation(.spring(response: 0.35, dampingFraction: 0.7)) {
                                vm.selectShizhi(shizhi)
                            }
                        }
                    }
                }
                .padding(.horizontal, 4)
                .padding(.vertical, 4)
            }
        }
    }

    // MARK: デバッグパネル（L14〜L27）
    private var debugPanel: some View {
        VStack(alignment: .leading, spacing: 12) {
            // パネルヘッダー
            HStack {
                Label("精密層フィルター", systemImage: "slider.horizontal.3")
                    .font(.system(size: 12, weight: .semibold))
                    .foregroundStyle(.white.opacity(0.6))
                    .tracking(1)
                Spacer()
                Text("L14〜L27  \(vm.filteredPreciseLayers.count)/\(LuopanLayer.preciseRange.count)層有効")
                    .font(.system(size: 11, weight: .medium, design: .monospaced))
                    .foregroundStyle(.white.opacity(0.35))
            }

            // レイヤーグリッド
            LazyVGrid(
                columns: [GridItem(.flexible()), GridItem(.flexible())],
                spacing: 8
            ) {
                ForEach(vm.allPreciseLayersWithState, id: \.layer.id) { item in
                    LayerCell(layer: item.layer, isActive: item.isActive)
                }
            }
        }
        .padding(16)
        .background(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(Color.black.opacity(0.3))
                .overlay(
                    RoundedRectangle(cornerRadius: 16, style: .continuous)
                        .stroke(Color.white.opacity(0.06), lineWidth: 1)
                )
        )
    }
}

// MARK: - 羅盤コンパスView

struct LuopanCompassView: View {
    let rotation: Double
    let shizhi: Shizhi

    // 二十四方位
    private let directions24 = [
        "子","癸","丑","艮","寅","甲",
        "卯","乙","辰","巽","巳","丙",
        "午","丁","未","坤","申","庚",
        "酉","辛","戌","乾","亥","壬"
    ]

    var body: some View {
        GeometryReader { geo in
            let size = min(geo.size.width, geo.size.height)
            let center = CGPoint(x: geo.size.width / 2, y: geo.size.height / 2)

            ZStack {
                // 最外リング：装飾
                Circle()
                    .stroke(
                        AngularGradient(
                            colors: [
                                Color(red: 0.8, green: 0.6, blue: 0.2),
                                Color(red: 0.4, green: 0.3, blue: 0.1),
                                Color(red: 0.8, green: 0.6, blue: 0.2),
                            ],
                            center: .center
                        ),
                        lineWidth: 2
                    )
                    .frame(width: size * 0.95, height: size * 0.95)

                // 二十四山リング（回転する）
                ZStack {
                    Circle()
                        .fill(Color(red: 0.10, green: 0.10, blue: 0.16))
                        .frame(width: size * 0.90, height: size * 0.90)

                    // 24方位ラベル
                    ForEach(0..<24, id: \.self) { i in
                        let angle = Double(i) * 15.0 - 90.0
                        let rad = angle * .pi / 180
                        let r = size * 0.38
                        let x = center.x + CGFloat(cos(rad)) * r - geo.size.width / 2
                        let y = center.y + CGFloat(sin(rad)) * r - geo.size.height / 2

                        Text(directions24[i])
                            .font(.system(size: size * 0.030, weight: i % 3 == 0 ? .bold : .thin, design: .serif))
                            .foregroundStyle(
                                i % 3 == 0
                                    ? Color(red: 0.95, green: 0.80, blue: 0.40)
                                    : Color.white.opacity(0.55)
                            )
                            .rotationEffect(.degrees(angle + 90))
                            .offset(x: x, y: y)
                    }

                    // 目盛り線（24分割）
                    ForEach(0..<24, id: \.self) { i in
                        let angle = Double(i) * 15.0
                        Rectangle()
                            .fill(Color.white.opacity(i % 3 == 0 ? 0.35 : 0.12))
                            .frame(width: 1, height: i % 3 == 0 ? size * 0.06 : size * 0.03)
                            .offset(y: -(size * 0.43))
                            .rotationEffect(.degrees(angle))
                    }
                }
                .rotationEffect(.degrees(rotation))
                .animation(.easeOut(duration: 1.2), value: rotation)

                // 中間リング：玄空盤ライン
                Circle()
                    .stroke(Color.white.opacity(0.08), lineWidth: 1)
                    .frame(width: size * 0.60, height: size * 0.60)

                // 内円：時支表示
                ZStack {
                    Circle()
                        .fill(
                            RadialGradient(
                                colors: [
                                    shizhi.primaryPurpose.color.opacity(0.15),
                                    Color.black.opacity(0.6),
                                ],
                                center: .center,
                                startRadius: 0,
                                endRadius: size * 0.22
                            )
                        )
                        .frame(width: size * 0.44, height: size * 0.44)

                    Circle()
                        .stroke(shizhi.primaryPurpose.color.opacity(0.4), lineWidth: 1)
                        .frame(width: size * 0.44, height: size * 0.44)

                    VStack(spacing: 2) {
                        Text(shizhi.name)
                            .font(.system(size: size * 0.095, weight: .thin, design: .serif))
                            .foregroundStyle(shizhi.primaryPurpose.color)
                        Text("時")
                            .font(.system(size: size * 0.030, weight: .ultraLight))
                            .foregroundStyle(.white.opacity(0.4))
                    }
                }

                // 方位指針（北 = 上）
                VStack(spacing: 0) {
                    // 北指針（赤）
                    Triangle()
                        .fill(Color.red.opacity(0.85))
                        .frame(width: size * 0.028, height: size * 0.16)
                    // 中心ドット
                    Circle()
                        .fill(Color.white)
                        .frame(width: size * 0.025, height: size * 0.025)
                    // 南指針（白）
                    Triangle()
                        .fill(Color.white.opacity(0.6))
                        .frame(width: size * 0.028, height: size * 0.12)
                        .rotationEffect(.degrees(180))
                }
            }
            .frame(width: geo.size.width, height: geo.size.height)
        }
    }
}

// 三角形シェイプ
struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        Path { p in
            p.move(to: CGPoint(x: rect.midX, y: rect.minY))
            p.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
            p.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
            p.closeSubpath()
        }
    }
}

// 背景装飾リング
struct BackgroundRingsView: View {
    var body: some View {
        ZStack {
            ForEach([0.4, 0.6, 0.8, 1.0], id: \.self) { scale in
                Circle()
                    .stroke(Color.white.opacity(0.015), lineWidth: 1)
                    .scaleEffect(scale)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .offset(y: -120)
    }
}

// MARK: - サブコンポーネント

struct PurposeBadge: View {
    let purpose: LuopanPurpose
    let isActive: Bool

    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: purpose.icon)
                .font(.system(size: 10))
            Text(purpose.rawValue)
                .font(.system(size: 11, weight: .medium))
        }
        .foregroundStyle(isActive ? purpose.color : .white.opacity(0.2))
        .padding(.horizontal, 10)
        .padding(.vertical, 5)
        .background(
            Capsule()
                .fill(isActive ? purpose.color.opacity(0.12) : Color.white.opacity(0.03))
                .overlay(
                    Capsule()
                        .stroke(isActive ? purpose.color.opacity(0.4) : Color.white.opacity(0.08), lineWidth: 1)
                )
        )
        .animation(.easeInOut(duration: 0.25), value: isActive)
    }
}

struct ShizhiChip: View {
    let shizhi: Shizhi
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 3) {
                Text(shizhi.name)
                    .font(.system(size: 15, weight: isSelected ? .semibold : .thin, design: .serif))
                    .foregroundStyle(isSelected ? shizhi.primaryPurpose.color : .white.opacity(0.55))
                Text(String(format: "%02d", shizhi.startHour))
                    .font(.system(size: 9, weight: .regular, design: .monospaced))
                    .foregroundStyle(.white.opacity(0.3))
            }
            .frame(width: 40, height: 46)
            .background(
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .fill(isSelected ? shizhi.primaryPurpose.color.opacity(0.15) : Color.white.opacity(0.04))
                    .overlay(
                        RoundedRectangle(cornerRadius: 10, style: .continuous)
                            .stroke(
                                isSelected ? shizhi.primaryPurpose.color.opacity(0.5) : Color.clear,
                                lineWidth: 1
                            )
                    )
            )
        }
        .buttonStyle(.plain)
    }
}

struct LayerCell: View {
    let layer: LuopanLayer
    let isActive: Bool

    private var primaryPurpose: LuopanPurpose? {
        // 表示上の代表色を決定
        if layer.purposes.contains(.liXiang)   { return .liXiang }
        if layer.purposes.contains(.geLong)    { return .geLong }
        if layer.purposes.contains(.shouShui)  { return .shouShui }
        return nil
    }

    var body: some View {
        HStack(spacing: 8) {
            // L番号
            Text("L\(layer.id)")
                .font(.system(size: 10, weight: .bold, design: .monospaced))
                .foregroundStyle(isActive ? (primaryPurpose?.color ?? .white) : .white.opacity(0.2))
                .frame(width: 28, alignment: .leading)

            VStack(alignment: .leading, spacing: 2) {
                Text(layer.name)
                    .font(.system(size: 11, weight: isActive ? .medium : .light))
                    .foregroundStyle(isActive ? .white.opacity(0.9) : .white.opacity(0.2))
                    .lineLimit(1)
                    .minimumScaleFactor(0.8)

                // 用途ドット
                HStack(spacing: 3) {
                    ForEach(LuopanPurpose.allCases, id: \.self) { p in
                        Circle()
                            .fill(layer.purposes.contains(p) && isActive ? p.color : Color.white.opacity(0.08))
                            .frame(width: 5, height: 5)
                    }
                    if layer.isPrecise {
                        Spacer()
                        Text("104")
                            .font(.system(size: 8, weight: .bold, design: .monospaced))
                            .foregroundStyle(isActive ? Color(red: 0.95, green: 0.80, blue: 0.40).opacity(0.8) : .white.opacity(0.1))
                    }
                }
            }

            Spacer(minLength: 0)

            // アクティブインジケーター
            Image(systemName: isActive ? "checkmark.circle.fill" : "circle")
                .font(.system(size: 13))
                .foregroundStyle(
                    isActive
                        ? (primaryPurpose?.color ?? .white).opacity(0.8)
                        : .white.opacity(0.1)
                )
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 8)
        .background(
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .fill(isActive ? Color.white.opacity(0.05) : Color.white.opacity(0.02))
                .overlay(
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .stroke(
                            isActive
                                ? (primaryPurpose?.color ?? .white).opacity(0.2)
                                : Color.white.opacity(0.05),
                            lineWidth: 1
                        )
                )
        )
        .animation(.easeInOut(duration: 0.3), value: isActive)
    }
}

// MARK: - 時支ピッカーSheet

struct ShizhiPickerSheet: View {
    @ObservedObject var vm: LuopanViewModel
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ZStack {
                Color(red: 0.06, green: 0.06, blue: 0.10).ignoresSafeArea()

                ScrollView {
                    LazyVGrid(
                        columns: Array(repeating: GridItem(.flexible(), spacing: 12), count: 3),
                        spacing: 12
                    ) {
                        ForEach(Shizhi.all) { shizhi in
                            ShizhiPickerCell(shizhi: shizhi, isSelected: vm.currentShizhi.id == shizhi.id) {
                                vm.selectShizhi(shizhi)
                                dismiss()
                            }
                        }
                    }
                    .padding(20)
                }
            }
            .navigationTitle("時支を選択")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button {
                        vm.enableAutoMode()
                        dismiss()
                    } label: {
                        Label("自動", systemImage: "clock.arrow.circlepath")
                            .font(.system(size: 13))
                    }
                    .tint(.green)
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("閉じる") { dismiss() }
                        .tint(.white.opacity(0.6))
                }
            }
            .preferredColorScheme(.dark)
        }
    }
}

struct ShizhiPickerCell: View {
    let shizhi: Shizhi
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                // 時支文字
                Text(shizhi.name)
                    .font(.system(size: 36, weight: .thin, design: .serif))
                    .foregroundStyle(isSelected ? shizhi.primaryPurpose.color : .white.opacity(0.7))

                Text(shizhi.timeRange)
                    .font(.system(size: 10, weight: .regular, design: .monospaced))
                    .foregroundStyle(.white.opacity(0.4))
                    .lineLimit(1)
                    .minimumScaleFactor(0.7)

                // 主用途バッジ
                HStack(spacing: 4) {
                    Image(systemName: shizhi.primaryPurpose.icon)
                        .font(.system(size: 9))
                    Text(shizhi.primaryPurpose.rawValue)
                        .font(.system(size: 10, weight: .medium))
                }
                .foregroundStyle(shizhi.primaryPurpose.color.opacity(isSelected ? 1.0 : 0.6))
                .padding(.horizontal, 8)
                .padding(.vertical, 3)
                .background(Capsule().fill(shizhi.primaryPurpose.color.opacity(0.12)))
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 16)
            .background(
                RoundedRectangle(cornerRadius: 14, style: .continuous)
                    .fill(isSelected ? shizhi.primaryPurpose.color.opacity(0.12) : Color.white.opacity(0.04))
                    .overlay(
                        RoundedRectangle(cornerRadius: 14, style: .continuous)
                            .stroke(
                                isSelected ? shizhi.primaryPurpose.color.opacity(0.5) : Color.white.opacity(0.08),
                                lineWidth: isSelected ? 1.5 : 1
                            )
                    )
            )
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Preview

#Preview {
    ContentView()
        .preferredColorScheme(.dark)
}
