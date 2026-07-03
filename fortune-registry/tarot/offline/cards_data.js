/* ======================================
   タロットデータ - JSON値 (registry/major.json をラップ)
   file:// 環境でのCORS対策用
   ====================================== */

const TAROT_CARDS_DATA = {
  "meta": {
    "version": "2.0.0",
    "description": "大アルカナ22枚の統合マスターデータ（構造化版・五行配当付き）",
    "last_updated": "2026-05-25",
    "note": "v2.0: 新構造(id, upright/reversed)を採用。既存のwuxing・element_note情報を統合。card_notes/配下の個別詳細ノートとの連携を想定。"
  },
  "cards": [
    {
      "id": "M00",
      "number": 0,
      "name_en": "The Fool",
      "name_ja": "愚者",
      "wuxing": "木",
      "element_note": "始まり・出発・春の芽吹き。制御されていない木気。",
      "upright": {
        "keywords": ["自由", "始まり", "純粋", "可能性"],
        "action_advice": "結果を恐れず、まずは直感に従って一歩を踏み出してみる時です。"
      },
      "reversed": {
        "keywords": ["無計画", "無責任", "優柔不断", "停滞"],
        "action_advice": "準備不足や焦りがないか、一度立ち止まって足元を確認してください。"
      }
    },
    {
      "id": "M01",
      "number": 1,
      "name_en": "The Magician",
      "name_ja": "魔術師",
      "wuxing": "火",
      "element_note": "意志・顕現・天と地を繋ぐ火の力。",
      "upright": {
        "keywords": ["創造", "技術", "自信", "集中"],
        "action_advice": "手元にある道具やスキルは十分揃っています。自信を持って計画を実行に移しましょう。"
      },
      "reversed": {
        "keywords": ["空回り", "不調装", "欺瞞", "未熟"],
        "action_advice": "小手先の技術や嘘で誤魔化さず、基礎スキルの磨き直しや準備の再確認をしてください。"
      }
    },
    {
      "id": "M02",
      "number": 2,
      "name_en": "The High Priestess",
      "name_ja": "女教皇",
      "wuxing": "水",
      "element_note": "隠れた知・直感・深い水。表に出ない力。",
      "upright": {
        "keywords": ["直感", "知性", "静寂", "客観性"],
        "action_advice": "周囲の雑音から離れ、自分の内なる直感と冷静な分析力に耳を傾けてください。"
      },
      "reversed": {
        "keywords": ["批判的", "神経質", "冷淡", "現実逃避"],
        "action_advice": "白黒ハッキリつけようと批判的になりがちです。寛容な心を持ち、感情の波を落ち着かせましょう。"
      }
    },
    {
      "id": "M03",
      "number": 3,
      "name_en": "The Empress",
      "name_ja": "女帝",
      "wuxing": "木",
      "element_note": "豊穣・育む木の陰。大地の生産力。",
      "upright": {
        "keywords": ["豊かさ", "包容力", "愛情", "生産性"],
        "action_advice": "現状を愛し、育てる時期です。周囲への感謝を形にし、心地よい環境作りに注力しましょう。"
      },
      "reversed": {
        "keywords": ["過保護", "我儘", "怠惰", "浪費"],
        "action_advice": "過剰な干渉や依存心が生じているサインです。甘えを捨て、自立心を取り戻してください。"
      }
    },
    {
      "id": "M04",
      "number": 4,
      "name_en": "The Emperor",
      "name_ja": "皇帝",
      "wuxing": "火",
      "element_note": "支配・権威・陽の極。秩序を作る火。",
      "upright": {
        "keywords": ["安定", "支配", "責任感", "リーダー"],
        "action_advice": "強い意思と責任感を持って主導権を握り、明確なルールや構造を確立してください。"
      },
      "reversed": {
        "keywords": ["独裁", "横暴", "無力感", "過労"],
        "action_advice": "頑固さや高圧的な態度で孤立を招いています。柔軟に周囲の意見を取り入れましょう。"
      }
    },
    {
      "id": "M05",
      "number": 5,
      "name_en": "The Hierophant",
      "name_ja": "法王",
      "wuxing": "土",
      "element_note": "伝統・制度・中央の土。橋渡しする力。",
      "upright": {
        "keywords": ["モラル", "信頼", "導き", "伝統"],
        "action_advice": "秩序や伝統的なルールを守り、信頼できる専門家や先輩にアドバイスを求めると道が開けます。"
      },
      "reversed": {
        "keywords": ["不信感", "偏見", "独善", "反発"],
        "action_advice": "視野が狭くなり、マニュアルに固執しています。柔軟でオープンな思考を意識してください。"
      }
    },
    {
      "id": "M06",
      "number": 6,
      "name_en": "The Lovers",
      "name_ja": "恋人",
      "wuxing": "木",
      "element_note": "選択・調和・木と木の共鳴。",
      "upright": {
        "keywords": ["選択", "調和", "情熱", "共感"],
        "action_advice": "自分の心が真に心地よいと感じる選択、および周囲との調和を最優先に決定してください。"
      },
      "reversed": {
        "keywords": ["不調和", "誘惑", "優柔不断", "不実"],
        "action_advice": "目先の誘惑や他人の意見に流されています。本当に大切な価値観が何か、選び直してください。"
      }
    },
    {
      "id": "M07",
      "number": 7,
      "name_en": "The Chariot",
      "name_ja": "戦車",
      "wuxing": "水",
      "element_note": "意志による制御・水を操る力。前進する気。",
      "upright": {
        "keywords": ["前進", "勝利", "克服", "自己制御"],
        "action_advice": "二面性のある葛藤をコントロールし、目標に向かって迷わず一気に突き進んでください。"
      },
      "reversed": {
        "keywords": ["暴走", "挫折", "空回り", "制御不能"],
        "action_advice": "エネルギーが空回り、あるいは暴走しています。一旦スピードを落とし、軌道修正を図りましょう。"
      }
    },
    {
      "id": "M08",
      "number": 8,
      "name_en": "Strength",
      "name_ja": "力",
      "wuxing": "火",
      "element_note": "内なる火・柔らかな意志の強さ。",
      "upright": {
        "keywords": ["忍耐", "包容力", "本能制御", "不屈"],
        "action_advice": "腕力ではなく、粘り強い忍耐力と自己コントロール、そして愛を持って課題に向き合ってください。"
      },
      "reversed": {
        "keywords": ["落胆", "自信喪失", "感情爆発", "妥協"],
        "action_advice": "プレッシャーに負けて弱気になっています。自分の感情（本能）を否定せず、受け入れることから始めてください。"
      }
    },
    {
      "id": "M09",
      "number": 9,
      "name_en": "The Hermit",
      "name_ja": "隠者",
      "wuxing": "土",
      "element_note": "孤独・内省・山上の土。静かに待つ力。",
      "upright": {
        "keywords": ["探求", "内省", "孤独", "慎重"],
        "action_advice": "外側の情報に惑わされず、一人の時間を確保して本質を深く見つめ直す必要があります。"
      },
      "reversed": {
        "keywords": ["閉鎖的", "偏屈", "邪推", "現実無視"],
        "action_advice": "自分の世界に閉じこもり、頑固になっています。心の扉を少し開き、客観的な現実に目を向けましょう。"
      }
    },
    {
      "id": "M10",
      "number": 10,
      "name_en": "Wheel of Fortune",
      "name_ja": "運命の輪",
      "wuxing": "木",
      "element_note": "巡る気・春夏秋冬の木の循環。",
      "upright": {
        "keywords": ["転換点", "好機", "幸運", "タイミング"],
        "action_advice": "状況が急激に好転する兆しです。ためらわずにこの変化の波に乗り、チャンスを掴んでください。"
      },
      "reversed": {
        "keywords": ["暗転", "タイミング悪", "抵抗", "不運"],
        "action_advice": "今は逆風のタイミングです。無理に流れを変えようと足掻かず、嵐が過ぎ去るのを待ちましょう。"
      }
    },
    {
      "id": "M11",
      "number": 11,
      "name_en": "Justice",
      "name_ja": "正義",
      "wuxing": "金",
      "element_note": "裁断・公正・金の剋する力。",
      "upright": {
        "keywords": ["公平", "バランス", "誠実", "決断"],
        "action_advice": "感情に流されず、因果関係を客観的に捉えて、公明正大で誠実な判断を下してください。"
      },
      "reversed": {
        "keywords": ["不公平", "偏見", "優柔不断", "不釣り合い"],
        "action_advice": "偏った見方や、不公平な扱いに不満が募っています。まずは自分自身の天秤が傾いていないか確認しましょう。"
      }
    },
    {
      "id": "M12",
      "number": 12,
      "name_en": "The Hanged Man",
      "name_ja": "吊るされた男",
      "wuxing": "水",
      "element_note": "停止・逆さまの視点・水の深さ。",
      "upright": {
        "keywords": ["試練", "視点変更", "献身", "一時停止"],
        "action_advice": "動けない現状を逆手に取り、物事を180度違う視点から捉え直すことで新しい智慧が得られます。"
      },
      "reversed": {
        "keywords": ["無駄な犠牲", "骨折り損", "自己憐憫", "執着"],
        "action_advice": "報われない努力や我慢に縛られています。「犠牲になっている」という被害者意識を手放してください。"
      }
    },
    {
      "id": "M13",
      "number": 13,
      "name_en": "Death",
      "name_ja": "死神",
      "wuxing": "水",
      "element_note": "終わりと始まり・冬の水。脱皮する力。",
      "upright": {
        "keywords": ["終わり", "再生", "リセット", "決別"],
        "action_advice": "役目を終えた古い状況や関係性を完全に手放してください。それは新しい始まりへの絶対条件です。"
      },
      "reversed": {
        "keywords": ["未練", "再生遅延", "惰性", "執着"],
        "action_advice": "終わったことに執着し、変化を拒んでいます。未練を断ち切り、強制終了を受け入れる覚悟を持ちましょう。"
      }
    },
    {
      "id": "M14",
      "number": 14,
      "name_en": "Temperance",
      "name_ja": "節制",
      "wuxing": "土",
      "element_note": "調和・中庸・水と火を合わせる土の働き。",
      "upright": {
        "keywords": ["調和", "循環", "適応", "錬金術"],
        "action_advice": "異なる要素をうまく調和させ、中庸を保ちましょう。穏やかなコミュニケーションが状況を好転させます。"
      },
      "reversed": {
        "keywords": ["不調和", "過剰", "不摂生", "消耗"],
        "action_advice": "生活や感情のバランスが崩れ、コントロールを失っています。過剰な要素を削ぎ落としてください。"
      }
    },
    {
      "id": "M15",
      "number": 15,
      "name_en": "The Devil",
      "name_ja": "悪魔",
      "wuxing": "土",
      "element_note": "執着・束縛・重い土の陰。",
      "upright": {
        "keywords": ["束縛", "欲望", "依存", "執着"],
        "action_advice": "目先の快楽や依存関係、固定観念に縛られています。自分が何に囚われているかを自覚しましょう。"
      },
      "reversed": {
        "keywords": ["覚醒", "束縛打破", "悪習慣改善", "自立"],
        "action_advice": "不健全な関係や悪習慣から抜け出すチャンスが到来しています。強い意志を持って自立の一歩を踏み出してください。"
      }
    },
    {
      "id": "M16",
      "number": 16,
      "name_en": "The Tower",
      "name_ja": "塔",
      "wuxing": "火",
      "element_note": "崩壊・雷火・急激な火の爆発。",
      "upright": {
        "keywords": ["崩壊", "劇的変化", "衝撃", "覚醒"],
        "action_advice": "既存のプライドや不都合な基盤が崩れ去りますが、これは嘘のない真実へ向かうための必要な崩壊です。"
      },
      "reversed": {
        "keywords": ["緊迫状態", "現状維持固執", "大難小難", "慢性ストレス"],
        "action_advice": "崩壊の危機を前にして、無理にしがみついています。根本原因を放置せず、抜本的な見直しを行ってください。"
      }
    },
    {
      "id": "M17",
      "number": 17,
      "name_en": "The Star",
      "name_ja": "星",
      "wuxing": "金",
      "element_note": "希望・浄化・夜空の金気。",
      "upright": {
        "keywords": ["希望", "インスピレーション", "純粋", "癒し"],
        "action_advice": "暗闇の中に希望の光が見えてきます。自らの理想や直感を信じて、純粋なビジョンを描き続けましょう。"
      },
      "reversed": {
        "keywords": ["幻滅", "高望み", "悲観的", "インスピ不足"],
        "action_advice": "理想が高すぎて現実とのギャップに落胆しています。まずは手の届く小さな現実から見つめ直しましょう。"
      }
    },
    {
      "id": "M18",
      "number": 18,
      "name_en": "The Moon",
      "name_ja": "月",
      "wuxing": "水",
      "element_note": "幻想・不安・満ち欠ける水の陰。",
      "upright": {
        "keywords": ["不安", "幻想", "見通し難", "潜在意識"],
        "action_advice": "先が見えず不安が募る時期ですが、無理に動くと迷走します。輪郭がはっきりするまで静観してください。"
      },
      "reversed": {
        "keywords": ["霧晴れる", "不安解消", "真実露見", "現実回帰"],
        "action_advice": "徐々に不透明だった状況から霧が晴れ、真実が見えてきます。確信を持って次の具体的な行動を起こしましょう。"
      }
    },
    {
      "id": "M19",
      "number": 19,
      "name_en": "The Sun",
      "name_ja": "太陽",
      "wuxing": "火",
      "element_note": "顕現・陽の極・万物を照らす火。",
      "upright": {
        "keywords": ["成功", "活力", "明確", "祝福"],
        "action_advice": "すべての問題が明るい光に照らされ解決します。エネルギー全開で自己表現し、喜びを周囲と共有しましょう。"
      },
      "reversed": {
        "keywords": ["不調", "延期", "陰り", "過信"],
        "action_advice": "完全な失敗ではないものの、パワー不足や計画の遅延が生じやすいです。過信を捨て、エネルギーを充電してください。"
      }
    },
    {
      "id": "M20",
      "number": 20,
      "name_en": "Judgement",
      "name_ja": "審判",
      "wuxing": "金",
      "element_note": "決断・召喚・金の断ち切る力。",
      "upright": {
        "keywords": ["復活", "覚醒", "吉報", "過去清算"],
        "action_advice": "過去の努力が報われ、再びチャンスが巡ってきます。心の声（使命）に従って、迷わず立ち上がってください。"
      },
      "reversed": {
        "keywords": ["再起不能", "後悔", "決定遅延", "見送り"],
        "action_advice": "過去の失敗を悔やみ、決断を先送りにしています。同じ過ちを繰り返さないと誓い、今度こそ前を向きましょう。"
      }
    },
    {
      "id": "M21",
      "number": 21,
      "name_en": "The World",
      "name_ja": "世界",
      "wuxing": "土",
      "element_note": "完成・統合・中央の土。すべてを包む。",
      "upright": {
        "keywords": ["完成", "統合", "達成", "完全なる調和"],
        "action_advice": "現在のサイクルは見事に完成へと至りました。この素晴らしい成果を祝い、次の新たなステージへ進む準備をしてください。"
      },
      "reversed": {
        "keywords": ["未完成", "中途半端", "マンネリ", "限界"],
        "action_advice": "ゴールの一歩手前で停滞、あるいは不完全燃焼を感じています。詰めが甘い部分がないか、最後の一踏ん張りを見せましょう。"
      }
    }
  ]
};

console.log('✓ cards_data.js が正常に読み込まれました。カード数:', TAROT_CARDS_DATA.cards.length, '枚');
