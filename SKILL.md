---
name: ameyodori-game
description: 「雨宿りの回廊（あめやどりのかいろう、Ameyodori no Kairou）」という個人開発の2DホラーパズルアクションWebゲームに関する話題が出たときに発動する。具体的には、Phaser 3で作るブラウザゲーム、商店街を舞台にしたホラー演出、姉弟キャラ（姉が主人公、弟が追従）、影の敵（shadow_enemy）、街灯・マッチ・鏡・押し箱・スイッチ・扉・隠し通路などの光と影のギミック、恐怖ゲージ（fear gauge）、手つなぎ（hand）システム、ドット絵アセット生成（Gemini向けプロンプト）、Pythonパッチスクリプトでのバージョン管理（v2〜v17）といった話題、あるいは「雨宿り」「ameyodori」「kairou」「回廊」「ホラーパズル」「Phaser ゲーム」などのキーワードが出たら発動する。
---

# 雨宿りの回廊 (Ameyodori no Kairou)

## プロジェクトの目的
雨の夜、無人の商店街でお母さんとはぐれた姉弟が出口を目指す、2Dホラー・パズルアクションWebゲーム。プレイヤーは姉を操作し、弟の手を引きながら、街灯の光を頼りに「影」から逃れて出口を探す。光と影をテーマにしたギミック（マッチで暗闇を照らす、鏡で光を反射する、街灯を点ける、隠し通路を見つける等）でパズルを解く構造。

個人開発（趣味プロジェクト）で、ブラウザだけで遊べる小規模ゲームとして完成させることを目指している。短時間で雰囲気とギミックを楽しめる体験が狙い。

## 現在のフェーズ
プロトタイプ開発中。最新は `ameyodori_v17.html`（単一HTMLにすべてが詰まっている形）。バージョンはv2〜v17まで反復してきており、`old_versions/` に過去版が保存されている。直近のコミットでv3〜v7、v17、ビルドスクリプト、Geminiプロンプト、game_assets画像が一括で追加された段階。

現状はPhaser側で `Graphics` を使ってドット絵テクスチャを動的生成しているが、`game_assets/` にGeminiで生成したPNG（sister, brother, shadow_enemy, floor, wall, streetlight）が用意されており、ここから「PNGアセットへの差し替え」が次の自然なステップに見える。3ステージ構成（`TOTAL_STAGES = 3`）が組まれており、ステージ別オーバーライド（`STAGE2_OVERRIDES`, `STAGE3_OVERRIDES`）でタイル配置を調整している。

## 技術スタック・使用ツール
- **Phaser 3** (3.60.0、CDN読み込み) — ゲームエンジン
- **JavaScript / HTML5 Canvas** — 単一HTMLファイル構成
- **Python 3** — `scripts/` 配下のパッチスクリプトで旧版HTMLから新版を生成（`make_v14.py`, `make_v16.py`, `patch_v15.py`, `patch1_constants.py` 〜 `patch6_fear_and_misc.py`）
- **Gemini** — ドット絵アセットの画像生成（`gemini_prompts.md` にバッチ別プロンプトを整備）
- **モバイル対応** — タッチコントロール用UI（`#mobile-controls`, `btn-hand`, `btn-match`）あり

## リポジトリ構成
- `/home/user/ameyodori-game/README.md` — プロジェクト概要（短い紹介のみ）
- `/home/user/ameyodori-game/ameyodori_v17.html` — **最新の本体**。Phaserのpreload/create/update、タイル定数、3ステージ生成ロジック、姉弟移動、影の敵、恐怖ゲージ、UI/HUDがすべてここに入っている
- `/home/user/ameyodori-game/ameyodori_v3.html` 〜 `ameyodori_v7.html` — ルートに残されている過去版（`old_versions/` にも同じものがある）
- `/home/user/ameyodori-game/old_versions/` — `ameyodori_v2.html` 〜 `ameyodori_v16.html` の歴代版アーカイブ
- `/home/user/ameyodori-game/game_assets/` — Geminiで生成したPNGアセット（`brother.png`, `sister.png`, `shadow_enemy.png`, `floor.png`, `wall.png`, `streetlight.png`）。**v17時点ではまだ未使用**で、現状はPhaserのGraphicsで動的生成
- `/home/user/ameyodori-game/scripts/` — 旧版HTMLにdiffを当てて新版を作るPythonスクリプト群。パッチは「定数追加 → テクスチャ → マップ → 移動 → buildStage → fear/misc」の順に分割されている
- `/home/user/ameyodori-game/gemini_prompts.md` — タイル/キャラ/敵を生成するためのGeminiプロンプト集（パレット指定 `#0a0a12, #1a1a2e, #ffdd88, #e08040, #4488cc, #661133, #08000f` 共通）

主要なゲーム内定数（v17）:
- タイル種別: `TILE_FLOOR=0, WALL=1, STREETLIGHT=2, MIRROR=3, SHOP=4, GOAL=5, PUSHBOX=6, BREAKLIGHT=7, SWITCH=8, DOOR=9, MATCH=10, HIDDEN=11, DARK=13`
- アクションキー: `E`（手をつなぐ／離す）、`F`（マッチを使う／`matchActive` を立てて `TILE_DARK` を通行可に）
- ステージ数: `TOTAL_STAGES = 3`

## Claudeに期待する役割
個人開発の議論相手・壁打ち相手として、以下のような相談に乗ってほしい:
- ゲームデザイン（恐怖演出、難易度曲線、ステージ構成、ギミックのアイデア出し）
- Phaser 3の実装相談（物理判定、タイルベース移動、シーン管理、テクスチャ生成 vs 画像読み込み）
- 単一HTMLという構成のまま続けるか、ファイル分割／ビルド化するかの判断
- `game_assets/` のPNGアセットを既存のGraphics生成と差し替える作業のレビュー
- v17 以降のリファクタ方針（バージョン番号運用、パッチスクリプト方式の継続可否）
- モバイルUX、タッチコントロールのチューニング
- ホラー演出（影の敵の挙動、サウンド、画面エフェクト）

「とりあえず動く」プロトタイプ段階なので、過剰な抽象化や大規模リファクタの提案より、**小さく確実に進める提案** を優先してほしい。

## 注意事項・前提
- 単一HTMLファイル（`ameyodori_v17.html`）にロジック・スタイル・マークアップが全部入っている。これは意図的な構成（配布が楽、個人開発で取り回しやすい）と思われるので、いきなり分割を提案するのは避ける
- `scripts/` 内のPythonスクリプトはパス（`C:\Users\kikai\OneDrive\Desktop\...`）がWindows絶対パスでハードコードされている。作者はWindows環境で作業している模様
- `scripts/` のパッチ方式は「旧版を取って→文字列置換で新版を作る」という方針。コードベース全体をいきなり書き換えるより、**小さなパッチを積み上げる進め方** に合わせる
- v17 はGraphics動的生成テクスチャを使っており、`game_assets/` のPNGはまだ統合されていない（次のマイルストーン候補）
- 共通カラーパレットは `gemini_prompts.md` の冒頭で固定されている（暗い青紫ベース、夜の雰囲気、8〜12色）。新しいアセット案を出すときはこのパレットに合わせる
- 言語は日本語ベース（タイトル・UI・コメント）。応答も基本は日本語で

## 調査手順
1. `README.md`、`CLAUDE.md`（※現時点では未作成）、`docs/`（※現時点では未作成）を全て読む
2. `gemini_prompts.md` でアートスタイルとアセット一覧を把握する
3. `scripts/` の `make_v16.py` と `patch_v15.py` を俯瞰して、バージョン間で何が変わったかを掴む
4. 最新版 `ameyodori_v17.html` のタイル定数・`buildStage` 関数・ステージオーバーライド・`update` ループを読む
5. コミット履歴の直近20件を見て、最近何に取り組んでいるか把握（※2026-04時点ではコミットは2件のみ：初期コミットと一括追加コミット）
6. 不明な点は推測せず「現時点では未定」と明記する
