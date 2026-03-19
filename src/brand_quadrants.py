"""
brand_quadrants.py — Brand quadrant classification and canonical name mapping.

Two-dimensional classification of ~200+ brands:
  - Price tier:        Generic vs. Premium  (based on avg_price + market positioning)
  - Social recognition: High vs. Low        (based on market presence + cultural familiarity)

Quadrants:
  household_giant     — High Recognition | Generic Price
  prestige_leader     — High Recognition | Premium Price
  niche_professional  — Low Recognition  | Premium Price
  local_value         — Low Recognition  | Generic Price
"""

import unicodedata

# ---------------------------------------------------------------------------
# Canonical brand name mapping: variant keyword → display name
# Used by _extract_brand_name() to merge duplicate entries.
# ---------------------------------------------------------------------------

BRAND_CANONICAL: dict[str, str] = {
    # Dairy variants
    'th true milk': 'TH True Milk',
    'th truemilk': 'TH True Milk',
    'thtrue': 'TH True Milk',
    'đà lạt milk': 'Dalat Milk',
    'dalat milk': 'Dalat Milk',
    'dalatmilk': 'Dalat Milk',
    'dutch lady': 'Dutch Lady',
    'cô gái hà lan': 'Dutch Lady',
    'binggrae': 'Binggrae',
    'bringrae': 'Binggrae',
    'président': 'Président',
    'president': 'Président',
    'presiden': 'Président',
    'ba vì': 'Ba Vì',
    'ba vi': 'Ba Vì',
    "love'in farm": "Love'in Farm",
    'love in farm': "Love'in Farm",

    # Seasoning / condiment variants
    'chinsu': 'Chin-Su',
    'chin-su': 'Chin-Su',
    'chin su': 'Chin-Su',
    'nam dương': 'Nam Dương',
    'nam duong': 'Nam Dương',
    'dh foods': 'DH Foods',
    'dhfoods': 'DH Foods',
    'dh food': 'DH Foods',

    # Ajinomoto family → single brand
    'ajinomoto': 'Ajinomoto',
    'aji-ngon': 'Ajinomoto',
    'aji-mayo': 'Ajinomoto',
    'aij - mayo': 'Ajinomoto',
    'aji-quick': 'Ajinomoto',

    # Nestlé variants
    'nestlé': 'Nestlé',
    'nestle': 'Nestlé',

    # Instant noodle variants
    'hảo hảo': 'Hảo Hảo',
    'hao hao': 'Hảo Hảo',

    # Frozen / processed variants
    'sg food': 'SG Food',
    'sgfood': 'SG Food',
    'sài gòn food': 'SG Food',
    'thực phẩm cầu tre': 'Cầu Tre',
    'cầu tre': 'Cầu Tre',
    'thaibifood': 'Thaibifood',
    'thabifood': 'Thaibifood',
    'hausubi': 'Hasubi',
    'hasubi': 'Hasubi',

    # Olivoilà variants
    'olivoilà': 'Olivoilà',
    'olivoila': 'Olivoilà',

    # Orion / Choco-pie → Orion
    'chocopie': 'Orion',
    'choco-pie': 'Orion',
    'choco pie': 'Orion',
    'orion': 'Orion',

    # Daesang variants
    'daesang': 'Daesang',
    'chungjungone': 'Daesang',

    # Angst / Trường Vinh
    'angst': 'Angst',
    'trường vinh': 'Angst',

    # Tao Kae Noi variants
    'tao kae noi': 'Taokeanoi',
    'taokeanoi': 'Taokeanoi',

    # Simply (trailing space in keywords)
    'simply ': 'Simply',

    # Doublemint / Wrigley → Wrigley
    'doublemint': 'Wrigley',
    'wrigley': 'Wrigley',
}


def _nkw(kw: str) -> str:
    return unicodedata.normalize('NFC', kw)


# NFC-normalize all keys at module load
BRAND_CANONICAL = {_nkw(k): v for k, v in BRAND_CANONICAL.items()}


# ---------------------------------------------------------------------------
# Brand quadrant assignments
# Maps canonical brand display name → quadrant string
# ---------------------------------------------------------------------------

BRAND_QUADRANTS: dict[str, str] = {
    # =======================================================================
    # 1. HOUSEHOLD GIANTS  (High Recognition | Generic Price)
    # =======================================================================
    'Vinamilk': 'household_giant',
    'Miwon': 'household_giant',
    'Meizan': 'household_giant',
    'Vifon': 'household_giant',
    'Fami': 'household_giant',
    'Vissan': 'household_giant',
    'Oishi': 'household_giant',
    'Tường An': 'household_giant',
    'Oreo': 'household_giant',
    'Orion': 'household_giant',
    "Lay'S": 'household_giant',
    'Hảo Hảo': 'household_giant',
    'Ajinomoto': 'household_giant',
    'Knorr': 'household_giant',
    'Maggi': 'household_giant',
    'Cholimex': 'household_giant',
    'Dutch Lady': 'household_giant',
    'Milo': 'household_giant',
    'Acecook': 'household_giant',
    'Chin-Su': 'household_giant',
    'Nam Ngư': 'household_giant',
    'Ba Vì': 'household_giant',
    'Simply': 'household_giant',
    'Neptune': 'household_giant',
    'Đức Việt': 'household_giant',
    'Nestlé': 'household_giant',
    'Cosy': 'household_giant',
    'Cô Gái Hà Lan': 'household_giant',  # alias for Dutch Lady kept for safety
    'Cầu Tre': 'household_giant',
    'Ông Thọ': 'household_giant',
    'Mộc Châu': 'household_giant',
    'Yomost': 'household_giant',
    'Kinh Đô': 'household_giant',
    'Bibica': 'household_giant',
    'Colgate': 'household_giant',
    'P/S': 'household_giant',
    'Vedan': 'household_giant',
    'Meatdeli': 'household_giant',
    'Cái Lân': 'household_giant',
    'Kewpie': 'household_giant',
    'Nam Dương': 'household_giant',
    'Biên Hòa': 'household_giant',

    # =======================================================================
    # 2. PRESTIGE LEADERS  (High Recognition | Premium Price)
    # =======================================================================
    'TH True Milk': 'prestige_leader',
    'Nutifood': 'prestige_leader',
    'Omachi': 'prestige_leader',
    'Pediasure': 'prestige_leader',
    'Ensure': 'prestige_leader',
    'Glucerna': 'prestige_leader',
    'Danisa': 'prestige_leader',
    'Meiji': 'prestige_leader',
    'Dalat Milk': 'prestige_leader',
    'Ovaltine': 'prestige_leader',
    'Cung Đình': 'prestige_leader',
    'Samyang': 'prestige_leader',
    'Lotte': 'prestige_leader',
    'Nutella': 'prestige_leader',
    'Similac': 'prestige_leader',
    'Unidry': 'prestige_leader',
    'Degrees': 'prestige_leader',
    'Indomie': 'prestige_leader',
    'Nongshim': 'prestige_leader',

    # =======================================================================
    # 3. NICHE PROFESSIONALS  (Low Recognition | Premium Price)
    # =======================================================================
    'Ferrero': 'niche_professional',
    'Merci': 'niche_professional',
    'Lindt': 'niche_professional',
    'Barilla': 'niche_professional',
    'Agnesi': 'niche_professional',
    'Anchor': 'niche_professional',
    'Président': 'niche_professional',
    'Westgold': 'niche_professional',
    'Ritter Sport': 'niche_professional',
    'Kellogg': 'niche_professional',
    'Matilde Vicenzi': 'niche_professional',
    'Arcor': 'niche_professional',
    'Leibniz': 'niche_professional',
    'Meadow Fresh': 'niche_professional',
    'Avonmore': 'niche_professional',
    'Devondale': 'niche_professional',
    'Lactacyd': 'niche_professional',
    'Kikkoman': 'niche_professional',
    'Lee Kum Kee': 'niche_professional',
    'Orifood': 'niche_professional',
    'Thaibifood': 'niche_professional',
    'Alpenliebe': 'niche_professional',
    'Ottogi': 'niche_professional',
    'Haribo': 'niche_professional',
    'Vinamit': 'niche_professional',
    'Đôi Đũa Vàng': 'niche_professional',
    'Ông Già Ika': 'niche_professional',
    'Farmers Union': 'niche_professional',
    'Bibigo': 'niche_professional',
    'Taokeanoi': 'niche_professional',
    'Zott': 'niche_professional',
    'Calbee': 'niche_professional',
    'Gullon': 'niche_professional',
    'M&M': 'niche_professional',
    'Pepperidge Farm': 'niche_professional',
    'Olivoilà': 'niche_professional',
    'Pringles': 'niche_professional',
    'Doritos': 'niche_professional',
    'Ricola': 'niche_professional',
    'Kinder': 'niche_professional',
    'Bahlsen': 'niche_professional',
    'Loacker': 'niche_professional',
    'Emborg': 'niche_professional',
    'Paysan Breton': 'niche_professional',
    'Borggreve': 'niche_professional',
    'S&B': 'niche_professional',
    'Sempio': 'niche_professional',
    'Yakult': 'niche_professional',
    'Marukome': 'niche_professional',
    'Wrigley': 'niche_professional',
    'Mccain': 'niche_professional',
    'Mcvitie': 'niche_professional',
    'Lambertz': 'niche_professional',
    'Spam': 'niche_professional',
    'Skittles': 'niche_professional',
    'Bega': 'niche_professional',
    'Tresor Dore': 'niche_professional',
    'Dole': 'niche_professional',
    'Fragata': 'niche_professional',
    'Huggies': 'niche_professional',
    'Binggrae': 'niche_professional',
    'Qbb': 'niche_professional',
    'Kameda': 'niche_professional',
    'Karamucho': 'niche_professional',
    'Sahmyook': 'niche_professional',
    'Betagen': 'niche_professional',
    'Oatta': 'niche_professional',
    'Tohogenkai': 'niche_professional',
    'Latino Bella': 'niche_professional',
    'Sunraysia': 'niche_professional',
    'Hồng Lam': 'niche_professional',
    'Lê Gia': 'niche_professional',
    'Home Food': 'niche_professional',
    'Celano': 'niche_professional',
    'Marukyo': 'niche_professional',
    'Le Gourmet': 'niche_professional',
    'Lutosa': 'niche_professional',
    'Ito': 'niche_professional',
    'Taeyung': 'niche_professional',
    'Khải Hoàn': 'niche_professional',
    'Vinabee': 'niche_professional',
    'Lof': 'niche_professional',
    'Lot 100': 'niche_professional',
    'Bakalland': 'niche_professional',
    'Johnson': 'niche_professional',
    'Carrie Junior': 'niche_professional',

    # =======================================================================
    # 4. LOCAL & VALUE PLAYERS  (Low Recognition | Generic Price)
    # =======================================================================
    'Ba Huân': 'local_value',
    'Dabaco': 'local_value',
    'Làng Mơ': 'local_value',
    'Sa Giang': 'local_value',
    'Mỹ Ngọc': 'local_value',
    'Vinafood': 'local_value',
    'Safoco': 'local_value',
    'Kim Bôi': 'local_value',
    'Senta': 'local_value',
    'Staff': 'local_value',
    'Bauli': 'local_value',
    'Karo': 'local_value',
    'Bento': 'local_value',
    'Pocky': 'local_value',
    'Toppo': 'local_value',
    'DH Foods': 'local_value',
    'Hey Yo': 'local_value',
    'Chef Biggy': 'local_value',
    'Hải Châu': 'local_value',
    'Lenger': 'local_value',
    'Seaspimex': 'local_value',
    'Con Bò Cười': 'local_value',
    'Barona': 'local_value',
    'Playmore': 'local_value',
    'Hoa Doanh': 'local_value',
    'Kun': 'local_value',
    'Koreno': 'local_value',
    'SG Food': 'local_value',
    'Hoàng Gia': 'local_value',
    'Angst': 'local_value',
    'Nutimilk': 'local_value',
    'Afc': 'local_value',
    'Ponnie': 'local_value',
    'Hải Nam': 'local_value',
    'Lc Food': 'local_value',
    'Xylitol': 'local_value',
    'Hoff': 'local_value',
    'Kitkool': 'local_value',
    'Thiên Nhiên Xanh': 'local_value',
    'Heo Cao Bồi': 'local_value',
    'Hạnh Phúc': 'local_value',
    'Lothamilk': 'local_value',
    'Richy': 'local_value',
    'Thuận Phát': 'local_value',
    'Ngọc Thơm': 'local_value',
    'Solite': 'local_value',
    'Phú Mỹ Bakery': 'local_value',
    'Golden Farm': 'local_value',
    'Tân Tân': 'local_value',
    'Minh Tiến': 'local_value',
    'Yến Việt': 'local_value',
    'Fristi': 'local_value',
    'Ông Kim': 'local_value',
    'Topkid': 'local_value',
    'Nuvi': 'local_value',
    'Nabati': 'local_value',
    'Solse': 'local_value',
    'Ông Kỳ': 'local_value',
    'Young Poong': 'local_value',
    'Thiên Lương': 'local_value',
    'Susu': 'local_value',
    'Ssh': 'local_value',
    'Probi': 'local_value',
    'Phạm Nghĩa': 'local_value',
    'Paldo': 'local_value',
    'Kokomi': 'local_value',
    'Kidsmix': 'local_value',
    'Long Nhi': 'local_value',
    'Bảo Ngọc': 'local_value',
    'Malai': 'local_value',
    'Biovegi': 'local_value',
    'Tân Việt Sin': 'local_value',
    'Vetrue': 'local_value',
    'Kiwifood': 'local_value',
    'Kiến Lĩnh': 'local_value',
    'Reeva': 'local_value',
    'Humanwell': 'local_value',
    'Tinh Nguyên': 'local_value',
    'Vietcoco': 'local_value',
    'Tâm Hòa': 'local_value',
    'Kopiko': 'local_value',
    'Mayora': 'local_value',
    'Lipzo': 'local_value',
    'Maruto': 'local_value',
    'Nissin': 'local_value',
    'Oral Clean': 'local_value',
    'Lactima': 'local_value',
    'Đế Vương': 'local_value',
    'Duyên Hải': 'local_value',
    'Thọ Phát': 'local_value',
    'Fasty': 'local_value',
    'Thanh Nga': 'local_value',
    'Three Lady Cooks': 'local_value',
    'Tic Tac': 'local_value',
    'Coba': 'local_value',
    'Trolli': 'local_value',
    'Corniche': 'local_value',
    'Vĩnh Thuận': 'local_value',
    'Daesang': 'local_value',
    'Cô Hường': 'local_value',
    'Green Sonka': 'local_value',
    'Hanns': 'local_value',
    'Ngôi Sao Phương Nam': 'local_value',
    'Orchid': 'local_value',
    'One-One': 'local_value',
    'Nuti Food': 'local_value',
    'Lilly': 'local_value',
    'Kronos': 'local_value',
    'Nanaco': 'local_value',
    'Momiji': 'local_value',
    'Mixxi': 'local_value',
    'Minh Hà': 'local_value',
    'Mikko': 'local_value',
    'Aquafresh': 'local_value',
    'Jordan': 'local_value',
    'Hanufood': 'local_value',
    'Jacker': 'local_value',
    'Tam Thái Tử': 'local_value',
    'Hasubi': 'local_value',
    'Hotpot Story': 'local_value',
    'Stfood': 'local_value',
    'Hồng Hạnh': 'local_value',
    'Anh Tuấn Khang': 'local_value',
    'Santa Lucia': 'local_value',
    'Kaka': 'local_value',
    'Kani Fresh': 'local_value',
    'Kani Supreme': 'local_value',
    'Reggia': 'local_value',
    'Bảo Minh': 'local_value',
    'An Vĩnh': 'local_value',
    'Tasami': 'local_value',
    'Godbawee': 'local_value',
    'Feddy': 'local_value',
    'Xuân An': 'local_value',
    'Minh Việt': 'local_value',
    'Ichiban': 'local_value',
    'Visaco': 'local_value',
    'Swing': 'local_value',
    'Chocopie': 'local_value',  # if listed separately from Orion
    'Choco-Pie': 'local_value',
    'Nue': 'local_value',
    'Listerine': 'local_value',
    'Bobby': 'local_value',
    'Sunmate': 'local_value',
    'Grow': 'local_value',
    "Love'in Farm": 'local_value',
    'Thanh Quốc': 'local_value',
    'Thanh Hà': 'local_value',
    'Cj Foods': 'local_value',
    'Reggia': 'local_value',

    # Extra single-product brands
    'Doublemint': 'local_value',

    # Brands that were missing from initial classification
    'Heinz': 'niche_professional',
    'Belcube': 'niche_professional',
    'Mentos': 'local_value',
    'Cadbury': 'niche_professional',
}

# Display labels for presentation
QUADRANT_LABELS: dict[str, str] = {
    'household_giant': 'Household Giant',
    'prestige_leader': 'Prestige Leader',
    'niche_professional': 'Niche Professional',
    'local_value': 'Local & Value',
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_quadrant(brand_name: str) -> str:
    """Return quadrant string for a brand, or empty string if unknown."""
    return BRAND_QUADRANTS.get(brand_name, '')


def is_premium(quadrant: str) -> int:
    """1 if brand is in a premium-price quadrant (prestige_leader or niche_professional)."""
    return int(quadrant in ('prestige_leader', 'niche_professional'))


def is_high_recognition(quadrant: str) -> int:
    """1 if brand is in a high-recognition quadrant (household_giant or prestige_leader)."""
    return int(quadrant in ('household_giant', 'prestige_leader'))
