"""
Central category configuration.

Each CategoryConfig holds the keyword map, priority order, and special-case rules
for one food category. The shared engine in src/categorize_core.py reads these configs
to run categorization without any category-specific code.

To add a new category:
  1. Define a CategoryConfig instance here.
  2. Add it to CATEGORY_REGISTRY.
  3. Create <NewCategory>/categorize.py and <NewCategory>/subcat_index.py from the templates
     in the existing thin-wrapper scripts.
"""

import unicodedata
from src.categorize_core import CategoryConfig

# ---------------------------------------------------------------------------
# Normalize helpers (reused by multiple categories)
# ---------------------------------------------------------------------------

def _nfc_lower(text) -> str:
    return unicodedata.normalize('NFC', str(text)).lower()

def _padded_nfc_lower(text) -> str:
    """NFC + lowercase + space-padding for word-boundary matching (Confectionary)."""
    return " " + unicodedata.normalize('NFC', str(text)).lower() + " "


# ---------------------------------------------------------------------------
# DAIRY
# ---------------------------------------------------------------------------
DAIRY = CategoryConfig(
    folder_name="Dairy",
    sub_map={
        "1": ["đậu nành", "đậu đen", "óc chó", "hạnh nhân", "mè đen", "gạo lứt", "bắp",
              "sữa hạt", "macca", "đậu đỏ", "lúa", "yến mạch", "milo", "ovaltine"],
        "2": ["sữa bột", "bột", "công thức", "ensure", "pedia", "grow", "similac",
              "colosbaby", "famna", "optimum", "pediasure", "glucerna", "nan ", "nuvi"],
        "3": ["bơ", "phô mai", "cheese", "bơ lạt", "bơ mặn", "bơ thực vật", "mascarpone",
              "cream cheese", "phomai", "kem sữa", "whipping", "cooking cream"],
        "4": ["sữa đặc", "ông thọ", "ngôi sao", "hoàn hảo", "creamer", "tài lộc"],
        "5": ["chua", "váng", "men vi", "probi", "yakult", "betagen", "susu", "kun", "yomost"],
    },
    priority_order=["5", "4", "1", "3", "2"],
    fallback="Sữa tươi",
    parent_label_code="Label 6",
    pre_check_fn=lambda n: "Sữa tươi" if "sữa trái cây" in n else None,
)

# ---------------------------------------------------------------------------
# BABY_PRODUCT
# ---------------------------------------------------------------------------
BABY_PRODUCT = CategoryConfig(
    folder_name="Baby_product",
    sub_map={
        "70": ["sữa bột", "dinh dưỡng", "vani", "ăn dặm", "bột", "sôcôla", "grow"],
        "71": ["tã", "bỉm", "tã quần", "tã dán", "lót"],
        "72": ["tắm", "gội", "phấn", "thân"],
    },
    priority_order=["70", "71", "72"],
    fallback="73",
    parent_label_code="Label 69",
)

# ---------------------------------------------------------------------------
# VEG_FRUIT
# ---------------------------------------------------------------------------
VEG_FRUIT = CategoryConfig(
    folder_name="Veg_Fruit",
    sub_map={
        "10": ["cam", "quất", "chanh", "xoài", "dưa hấu", "dưa lưới", "dưa lê",
               "thanh long", "chôm chôm", "hồng xiêm", "sapo", "kiwi", "chuối",
               "bưởi", "nho", "lê", "táo", "dứa", "khóm", "mận", "việt quất",
               "dâu", "chà là", "dừa xiêm", "dừa tiện lợi", "cherry", "đu đủ", "ổi"],
        "8":  ["cải", "rau", "xà lách", "giá đỗ", "hẹ lá", "hành lá",
               "cần tây", "cần nước", "ngọn", "lá", "húng", "mùi tàu", "mùi ta", "ngò", "dọc mùng"],
        "9":  ["nấm", "măng", "su hào", "bí", "khoai", "củ cải", "su su", "cà tím",
               "ngô", "đậu bắp", "đậu cove", "cà rốt", "hành củ", "hành lý sơn",
               "tỏi", "củ gừng", "củ sả", "củ nghệ", "củ riềng", "ớt",
               "hạt sen", "thực phẩm hỗn hợp", "cà chua"],
    },
    priority_order=["10", "8", "9"],
    fallback="9",
    parent_label_code="Label 7",
    normalize_fn=_nfc_lower,
)

# ---------------------------------------------------------------------------
# CONFECTIONARY
# ---------------------------------------------------------------------------
CONFECTIONARY = CategoryConfig(
    folder_name="Confectionary",
    sub_map={
        "31": ["kẹo", "socola", "chocolate", "sô cô la", "scl", "chobisca",
               "thạch", "jelly", "marshmallow", "marsmallows", "gum", "xylitol", "mentos", "tictac"],
        "32": ["snack", "khoai tây", "pringles", "lay", "ostar", "mực tẩm", "bento",
               "bánh que", "marine boy", "doakbua", "akiko", "bim bim", "swing",
               "doritos", "karamucho", "talaethong"],
        "33": ["ô mai ", "sấy", "nho khô", "hướng dương", "hạt bí", "hạt sen",
               "chà là", "mứt", "trái cây khô", "hạt điều", "đậu phộng", "đậu tỏi", "hạnh nhân",
               "hạt dẻ", "macca", "macadamia", "óc chó", "bò khô", "khô bò", "yến nhung"],
        "30": ["bánh quy", "bánh xốp", "bánh gạo", "chocopie", "custas", "bánh quế",
               "bánh bông lan", "solite", "bánh trứng", "tipo", "bánh dừa", "mochi",
               "bánh", "gouté", "danisa", "cosy", "oreo", "afc", "kenju", "bắp chiên"],
    },
    priority_order=["31", "32", "33", "30"],
    fallback="30",
    parent_label_code="Label 29",
    normalize_fn=_padded_nfc_lower,
    junk_keywords=["kem đánh răng"],
)

# ---------------------------------------------------------------------------
# DRY_FOOD
# ---------------------------------------------------------------------------
DRY_FOOD = CategoryConfig(
    folder_name="Dry_Food",
    sub_map={
        "52": ["chay", "thực phẩm chay", "âu lạc", "an nhiên"],
        "50": ["rong biển", "tảo", "lá kim", "rong nho", "kimnori", "kimbap",
               "cuộn cơm", "tokyolin", "r ong", "lá"],
        "51": ["bột", "thạch", "sương sáo", "nêm sẵn", "aji-quick", "chiên giòn",
               "chiên xù", "làm bánh", "pancake", "bánh rán"],
        "48": ["yến mạch", "ngũ cốc", "corn flakes", "muesli", "granola", "oatta",
               "kellogg", "nestlé", "milo", "froot loops", "koko krunch", "honey star",
               "calbee", "ngũ cốc", "oats"],
        "47": ["gạo", "nếp", "đậu xanh", "đậu đen", "đậu đỏ", "hạt sen", "lạc nhân",
               "hạt điều", "đậu phộng", "mè", "vừng", "nông sản", "nấm", "mộc nhĩ",
               "măng khô", "đỗ", "hạt"],
        "49": ["pate", "cá", "heo hầm", "bò hầm", "thịt xay", "thịt hộp", "spam",
               "tép", "tôm", "mực", "dưa chuột ngâm", "mứt", "bơ đậu phộng", "oliu",
               "bơ thực vật", "xúc xích", "thịt viên", "cà chua", "đóng hộp", "lon",
               "lọ", "hũ", "ruốc", "nutella", "phết", "cacao",
               "thịt áp chảo", "heo cao bồi", "ponnie", "cột đèn",
               "xốt", "gia vị", "nước mắm", "kho quẹt",
               "rim", "sấy giòn", "ăn liền", "tẩm gia vị"],
    },
    priority_order=["52", "50", "51", "48", "47", "49"],
    fallback="46",
    parent_label_code="Label 46",
    exclusion_map={"47": ["bơ"]},  # "bơ đậu phộng" must not match label 47
)

# ---------------------------------------------------------------------------
# EGG_AND_SOY
# ---------------------------------------------------------------------------
EGG_AND_SOY = CategoryConfig(
    folder_name="Egg_and_soy",
    sub_map={
        "68": ["đậu hũ", "tàu hũ", "đậu phụ", "đậu thanh", "tafu", "tofu",
               "đậu non", "đậu mơ", "đâu"],
        "67": ["trứng", "hột gà", "hột vịt", "quả"],
    },
    priority_order=["68", "67"],
    fallback="66",
    parent_label_code="Label 66",
)

# ---------------------------------------------------------------------------
# FROZEN
# ---------------------------------------------------------------------------
FROZEN = CategoryConfig(
    folder_name="Frozen",
    sub_map={
        "62": ["chả giò", "chả", "giò"],
        "63": ["viên", "mọc", "thả lẩu"],
        "64": ["bánh", "pizza", "há cảo", "xíu mại", "khoai", "lẩu", "phô mai que",
               "sủi cảo", "mandoo", "nugget", "rau", "nấm", "mỳ ý", "cơm chiên",
               "xôi", "chả ốc", "nem", "xúc xích", "lạp xưởng"],
        "60": ["hải sản", "tôm", "mực", "cá", "nghêu", "sò", "ốc", "hến", "hàu",
               "cua", "ghẹ", "surimi", "thanh cua", "bạch tuộc", "chả mực", "tép", "lươn"],
        "61": ["thịt", "bò", "heo", "gà", "trâu", "dồi", "ba chỉ", "lõi vai", "bắp", "steak"],
    },
    priority_order=["62", "63", "64", "60", "61"],
    fallback="Thực Phẩm Đông Lạnh Khác",
    parent_label_code="Label 65",
)

# ---------------------------------------------------------------------------
# INSTANT_FOOD
# ---------------------------------------------------------------------------
INSTANT_FOOD = CategoryConfig(
    folder_name="Instant_food",
    sub_map={
        "44": ["cháo", "soup", "súp", "chao to yen", "chao thit"],
        "45": ["phở", "bún", "bun bo", "bun rieu", "pho bo", "pho ga"],
        "43": ["miến", "hủ tíu", "hủ tiếu", "bánh canh", "bánh đa", "mien dong"],
        "42": ["mì", "mỳ", "nui", "spaghetti", "pasta",
               "tokpokki", "topokki", "bánh gạo",
               "ramen", "udon", "yakisoba", "kimchi",
               "omachi", "kokomi", "hảo hảo", "vifon", "acecook", "indomie", "koreno", "meizan"],
    },
    priority_order=["44", "45", "43", "42"],
    fallback="42",
    parent_label_code="Label 41",
    normalize_fn=_nfc_lower,
)

# ---------------------------------------------------------------------------
# PROCESSED_FOOD
# ---------------------------------------------------------------------------
PROCESSED_FOOD = CategoryConfig(
    folder_name="Processed_food",
    sub_map={
        "56": ["bánh bao"],
        "54": ["bánh mì", "banh my", "sandwich", "sanwhich", "bánh sừng bò"],
        "57": ["kim chi"],
        "55": ["xúc xích", "xx", "lạp xưởng", "lạp sườn",
               "thịt nguội", "ba rọi", "ba chỉ", "xông khói", "hun khói", "hong khói",
               "dăm bông", "jambong", "thăn lưng", "salami", "chân giò", "bắp bò", "gà tây",
               "thịt lợn hun khói", "gà muối", "tai heo muối"],
        "58": ["bánh trứng", "karo", "bánh pía", "bánh cốm", "bánh bông lan", "dorayaki",
               "bánh phồng tôm", "bánh ngon", "bánh đậu", "thanh cơm lứt", "tráng", "bánh chưng",
               "bông lan",
               "khô bò", "khô gà", "chà bông", "chân gà", "da cá", "nugget", "nem bùi", "bóng bì",
               "chả cốm", "măng muối", "gà xì dầu", "trà sữa", "thạch đen", "sữa bắp"],
    },
    priority_order=["56", "54", "57", "55", "58"],
    fallback="58",
    parent_label_code="Label 53",
    normalize_fn=_nfc_lower,
)

# ---------------------------------------------------------------------------
# SPICE — no categorize.py (single "Gia Vị" subcategory, handled differently)
# subcat_index.py for Spice does not use a lookup table and is kept as-is.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Registry — add new categories here
# ---------------------------------------------------------------------------
CATEGORY_REGISTRY = {
    "Dairy":         DAIRY,
    "Baby_product":  BABY_PRODUCT,
    "Veg_Fruit":     VEG_FRUIT,
    "Confectionary": CONFECTIONARY,
    "Dry_Food":      DRY_FOOD,
    "Egg_and_soy":   EGG_AND_SOY,
    "Frozen":        FROZEN,
    "Instant_food":  INSTANT_FOOD,
    "Processed_food": PROCESSED_FOOD,
}
