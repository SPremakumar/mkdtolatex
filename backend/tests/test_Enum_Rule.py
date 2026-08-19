from Enum_Rule import Rule

def test_nombre_de_regles():
    assert len(Rule) == 17


def test_regles_principales():
    assert Rule.DOCUMENT
    assert Rule.BLOCK
    assert Rule.HEADING
    assert Rule.PARAGRAPH
    assert Rule.INLINE
    assert Rule.IMAGE
    assert Rule.LINK
    assert Rule.TABLE
    assert Rule.CODE_BLOCK
    assert Rule.EOF


def test_regles_uniques():
    valeurs = [rule.value for rule in Rule]
    assert len(valeurs) == len(set(valeurs))


def test_rule_est_un_enum():
    for rule in Rule:
        assert isinstance(rule, Rule)


def test_conversion_depuis_le_nom():
    assert Rule["DOCUMENT"] == Rule.DOCUMENT
    assert Rule["HEADING"] == Rule.HEADING
    assert Rule["PARAGRAPH"] == Rule.PARAGRAPH
    assert Rule["EOF"] == Rule.EOF