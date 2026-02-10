from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from spots.models import Spot


class Command(BaseCommand):
    help = "Seed default spots (create/update + optional images)"

    def handle(self, *args, **options):
        
        images_dir = Path(settings.BASE_DIR) / "spots" / "seed_images"

        field_names = {f.name for f in Spot._meta.get_fields() if hasattr(f, "name")}

        def put(d: dict, key: str, value):
            if key in field_names:
                d[key] = value

        seeds = [
            {
                "name": "清水寺",
                "address": "京都府京都市東山区清水1-294",
                "phone": "075-551-1234",
                "website": "https://www.kiyomizudera.or.jp/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun"],
                "open_time": "06:00",
                "close_time": "18:00",
                "access": "最寄り駅から徒歩圏内",
                "language": "",
                "mood": "しっとり",
                "purpose": "神社/仏閣",
                "time_axis": "午前",
                "keywords": "京都,寺,世界遺産",
                "parking": "注意（公式HP参照）",
                "description": "京都を代表する寺院。季節の景色が人気。",
                "image_filename": "kiyomizudera.jpg",
            },
            {
                "name": "伏見稲荷大社",
                "address": "京都府京都市伏見区深草薮之内町68",
                "phone": "",
                "website": "https://inari.jp/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun","holiday"],
                "open_time": "00:00",
                "close_time": "23:59",
                "access": "最寄り駅から徒歩圏内",
                "language": "",
                "mood": "ワクワク",
                "purpose": "神社/仏閣",
                "time_axis": "午前",
                "keywords": "千本鳥居,京都",
                "parking": "注意（公式HP参照）",
                "description": "千本鳥居で有名。早朝が比較的空いています。",
                "image_filename": "fushimi_inari.jpg",
            },
            {
                "name": "金閣寺",
                "address": "京都府京都市北区金閣寺町1",
                "phone": "",
                "website": "https://www.shokoku-ji.jp/kinkakuji/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun"],
                "open_time": "09:00",
                "close_time": "17:00",
                "access": "バスでアクセス可",
                "language": "",
                "mood": "落ち着く",
                "purpose": "神社/仏閣",
                "time_axis": "午後",
                "keywords": "京都,寺,観光",
                "parking": "注意（公式HP参照）",
                "description": "金色に輝く舎利殿が印象的。",
                "image_filename": "kinkakuji.jpg",
            },
            {
                "name": "道頓堀",
                "address": "大阪府大阪市中央区道頓堀",
                "phone": "",
                "website": "https://www.osaka-info.jp/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun","holiday"],
                "open_time": "00:00",
                "close_time": "23:59",
                "access": "最寄り駅から徒歩圏内",
                "language": "",
                "mood": "にぎやか",
                "purpose": "グルメ/街歩き",
                "time_axis": "夜",
                "keywords": "大阪,グリコ,食べ歩き",
                "parking": "不明",
                "description": "大阪らしさ満点の繁華街。夜の散策が楽しい。",
                "image_filename": "dotonbori.jpg",
            },
            {
                "name": "大阪城",
                "address": "大阪府大阪市中央区大阪城1-1",
                "phone": "",
                "website": "https://www.osakacastle.net/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun"],
                "open_time": "09:00",
                "close_time": "17:00",
                "access": "最寄り駅から徒歩圏内",
                "language": "",
                "mood": "学び",
                "purpose": "歴史/観光",
                "time_axis": "午後",
                "keywords": "大阪,城,公園",
                "parking": "注意（公式HP参照）",
                "description": "天守閣と広い公園が魅力。",
                "image_filename": "osaka_castle.jpg",
            },
            {
                "name": "奈良公園",
                "address": "奈良県奈良市春日野町ほか",
                "phone": "",
                "website": "https://www3.pref.nara.jp/park/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun","holiday"],
                "open_time": "00:00",
                "close_time": "23:59",
                "access": "バスでアクセス可",
                "language": "",
                "mood": "のんびり",
                "purpose": "散歩/自然",
                "time_axis": "午前",
                "keywords": "鹿,奈良,公園",
                "parking": "注意（公式HP参照）",
                "description": "鹿と一緒に散策できる公園エリア。",
                "image_filename": "nara_park.jpg",
            },
            {
                "name": "姫路城",
                "address": "兵庫県姫路市本町68",
                "phone": "",
                "website": "https://www.himejicastle.jp/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun"],
                "open_time": "09:00",
                "close_time": "17:00",
                "access": "最寄り駅から徒歩圏内",
                "language": "",
                "mood": "感動",
                "purpose": "歴史/観光",
                "time_axis": "午後",
                "keywords": "世界遺産,城,兵庫",
                "parking": "注意（公式HP参照）",
                "description": "白鷺城として知られる名城。",
                "image_filename": "himeji_castle.jpg",
            },
            {
                "name": "神戸ハーバーランド",
                "address": "兵庫県神戸市中央区東川崎町",
                "phone": "",
                "website": "https://www.harborland.co.jp/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun","holiday"],
                "open_time": "10:00",
                "close_time": "21:00",
                "access": "最寄り駅から徒歩圏内",
                "language": "",
                "mood": "デート",
                "purpose": "買い物/夜景",
                "time_axis": "夕方",
                "keywords": "神戸,夜景,ショッピング",
                "parking": "有",
                "description": "海辺の商業エリア。夜景も人気。",
                "image_filename": "kobe_harborland.jpg",
            },
            {
                "name": "厳島神社",
                "address": "広島県廿日市市宮島町1-1",
                "phone": "",
                "website": "https://www.itsukushimajinja.jp/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun"],
                "open_time": "06:30",
                "close_time": "18:00",
                "access": "フェリーで移動",
                "language": "",
                "mood": "しっとり",
                "purpose": "神社/絶景",
                "time_axis": "午前",
                "keywords": "宮島,大鳥居,広島",
                "parking": "注意（公式HP参照）",
                "description": "海に浮かぶ大鳥居が有名。",
                "image_filename": "itsukushima.jpg",
            },
            {
                "name": "黒門市場",
                "address": "大阪府大阪市中央区日本橋2-4-1",
                "phone": "",
                "website": "https://www.kuromon.com/",
                "business_days": ["mon","tue","wed","thu","fri","sat","sun","irregular"],
                "open_time": "09:00",
                "close_time": "18:00",
                "access": "最寄り駅から徒歩圏内",
                "language": "",
                "mood": "にぎやか",
                "purpose": "食べ歩き",
                "time_axis": "昼",
                "keywords": "大阪,市場,グルメ",
                "parking": "不明",
                "description": "食べ歩きが楽しい市場。",
                "image_filename": "kuromon.jpg",
            },
        ]

        created = 0
        updated = 0
        images_applied = 0

        for s in seeds:
            defaults = {}
            put(defaults, "address", s.get("address", ""))
            put(defaults, "phone", s.get("phone", ""))
            put(defaults, "website", s.get("website", ""))
            put(defaults, "business_days", s.get("business_days", []))
            put(defaults, "open_time", s.get("open_time"))
            put(defaults, "close_time", s.get("close_time"))
            put(defaults, "access", s.get("access", ""))
            put(defaults, "language", s.get("language", ""))
            put(defaults, "mood", s.get("mood", ""))
            put(defaults, "purpose", s.get("purpose", ""))
            put(defaults, "time_axis", s.get("time_axis", ""))
            put(defaults, "keywords", s.get("keywords", ""))
            put(defaults, "parking", s.get("parking", "不明"))
            put(defaults, "description", s.get("description", ""))

            obj, is_created = Spot.objects.update_or_create(
                name=s["name"],
                defaults=defaults,
            )

            if "image" in field_names:
                filename = s.get("image_filename")
                if filename:
                    image_path = images_dir / filename
                    if image_path.exists():
                        if is_created or not getattr(obj, "image", None):
                            with open(image_path, "rb") as f:
                                obj.image.save(filename, File(f), save=True)
                            images_applied += 1

            if is_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"seed 完了: 新規 {created} 件 / 更新 {updated} 件 / 画像反映 {images_applied} 件"
            )
        )
