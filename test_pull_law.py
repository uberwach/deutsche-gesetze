from pull_law import extract_from_div
from lxml import html


HTML_BGB_13 = """
<div class="jnnorm" id="BJNR001950896BJNE244602360" title="Einzelnorm"><div class="jnheader"> <a name="BJNR001950896BJNE244602360"></a><a href="index.html#BJNR001950896BJNE244602360">Nichtamtliches Inhaltsverzeichnis</a><h3><span class="jnenbez">§ 13</span>&nbsp;<span class="jnentitel">Verbraucher</span></h3> </div>
<div><div class="jnhtml"><div><div class="jurAbsatz">Verbraucher ist jede natürliche Person, die ein Rechtsgeschäft zu Zwecken abschließt, die überwiegend weder ihrer gewerblichen noch ihrer selbständigen beruflichen Tätigkeit zugerechnet werden können.</div></div></div></div></div>
"""


def test_parse_norm():
    BGB_13_DIV = html.fromstring(HTML_BGB_13)
    result = extract_from_div(BGB_13_DIV)
    assert isinstance(result, dict)
    assert result.keys() == {"type", "norm", "title", "paragraphs"}
    assert result["type"] == "norm"
    assert result["norm"] == "§ 13"
    assert result["title"] == "Verbraucher"
    assert len(result["paragraphs"]) == 1


HTML_BGB_27 = """
<div class="jnnorm" id="BJNR001950896BJNE001803308" title="Einzelnorm"><div class="jnheader"> <a name="BJNR001950896BJNE001803308"></a><a href="index.html#BJNR001950896BJNE001803308">Nichtamtliches Inhaltsverzeichnis</a><h3><span class="jnenbez">§ 27</span>&nbsp;<span class="jnentitel">Bestellung und Geschäftsführung des Vorstands</span></h3> </div>
<div><div class="jnhtml"><div><div class="jurAbsatz">(1) Die Bestellung des Vorstands erfolgt durch Beschluss der Mitgliederversammlung.</div><div class="jurAbsatz">(2) Die Bestellung ist jederzeit widerruflich, unbeschadet des Anspruchs auf die vertragsmäßige Vergütung. Die Widerruflichkeit kann durch die Satzung auf den Fall beschränkt werden, dass ein wichtiger Grund für den Widerruf vorliegt; ein solcher Grund ist insbesondere grobe Pflichtverletzung oder Unfähigkeit zur ordnungsmäßigen Geschäftsführung.</div><div class="jurAbsatz">(3) Auf die Geschäftsführung des Vorstands finden die für den Auftrag geltenden Vorschriften der §§ 664 bis 670 entsprechende Anwendung. Die Mitglieder des Vorstands sind unentgeltlich tätig.</div></div></div></div></div>
"""


def test_parse_several_paragraph_norm():
    BGB_27_DIV = html.fromstring(HTML_BGB_27)
    result = extract_from_div(BGB_27_DIV)

    paragraphs = result["paragraphs"]

    assert 3 == len(paragraphs)


HTML_BGB_81 = """
<div class="jnnorm" id="BJNR001950896BJNE007204308" title="Einzelnorm"><div class="jnheader"> <a name="BJNR001950896BJNE007204308"></a><a href="index.html#BJNR001950896BJNE007204308">Nichtamtliches Inhaltsverzeichnis</a><h3><span class="jnenbez">§ 81</span>&nbsp;<span class="jnentitel">Stiftungsgeschäft</span></h3> </div>
<div><div class="jnhtml"><div><div class="jurAbsatz">(1) Das Stiftungsgeschäft unter Lebenden bedarf der schriftlichen Form. Es muss die verbindliche Erklärung des Stifters enthalten, ein Vermögen zur Erfüllung eines von ihm vorgegebenen Zweckes zu widmen, das auch zum Verbrauch bestimmt werden kann. Durch das Stiftungsgeschäft muss die Stiftung eine Satzung erhalten mit Regelungen über <dl style="font-weight:normal;font-style:normal;text-decoration:none;"><dt>1.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>den Namen der Stiftung,</div></dd><dt>2.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>den Sitz der Stiftung,</div></dd><dt>3.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>den Zweck der Stiftung,</div></dd><dt>4.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>das Vermögen der Stiftung,</div></dd><dt>5.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>die Bildung des Vorstands der Stiftung.</div></dd></dl>Genügt das Stiftungsgeschäft den Erfordernissen des Satzes 3 nicht und ist der Stifter verstorben, findet § 83 Satz 2 bis 4 entsprechende Anwendung.</div><div class="jurAbsatz">(2) Bis zur Anerkennung der Stiftung als rechtsfähig ist der Stifter zum Widerruf des Stiftungsgeschäfts berechtigt. Ist die Anerkennung bei der zuständigen Behörde beantragt, so kann der Widerruf nur dieser gegenüber erklärt werden. Der Erbe des Stifters ist zum Widerruf nicht berechtigt, wenn der Stifter den Antrag bei der zuständigen Behörde gestellt oder im Falle der notariellen Beurkundung des Stiftungsgeschäfts den Notar bei oder nach der Beurkundung mit der Antragstellung betraut hat.</div></div></div></div></div>
"""

def test_parse_sub_paragraph_norm():
    BGB_81_DIV = html.fromstring(HTML_BGB_81)
    result = extract_from_div(BGB_81_DIV)

    paragraphs = result["paragraphs"]

    assert 2 == len(paragraphs)

    first_paragraph = paragraphs[0]
    assert len(first_paragraph["sub"]) == 5
    assert len(first_paragraph["text"]) > 42


HTML_BGB_207 = """
<div class="jnnorm" id="BJNR001950896BJNE019904140" title="Einzelnorm"><div class="jnheader"> <a name="BJNR001950896BJNE019904140"></a><a href="index.html#BJNR001950896BJNE019904140">Nichtamtliches Inhaltsverzeichnis</a><h3><span class="jnenbez">§ 207</span>&nbsp;<span class="jnentitel">Hemmung der Verjährung aus familiären und ähnlichen Gründen</span></h3> </div>
<div><div class="jnhtml"><div><div class="jurAbsatz">(1) Die Verjährung von Ansprüchen zwischen Ehegatten ist gehemmt, solange die Ehe besteht. Das Gleiche gilt für Ansprüche zwischen <dl style="font-weight:normal;font-style:normal;text-decoration:none;"><dt>1.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>Lebenspartnern, solange die Lebenspartnerschaft besteht,</div></dd><dt>2.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>dem Kind und <dl><dt>a)</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>seinen Eltern oder</div></dd><dt>b)</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>dem Ehegatten oder Lebenspartner eines Elternteils</div></dd></dl>bis zur Vollendung des 21. Lebensjahres des Kindes,</div></dd><dt>3.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>dem Vormund und dem Mündel während der Dauer des Vormundschaftsverhältnisses,</div></dd><dt>4.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>dem Betreuten und dem Betreuer während der Dauer des Betreuungsverhältnisses und</div></dd><dt>5.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>dem Pflegling und dem Pfleger während der Dauer der Pflegschaft.</div></dd></dl>Die Verjährung von Ansprüchen des Kindes gegen den Beistand ist während der Dauer der Beistandschaft gehemmt.</div><div class="jurAbsatz">(2) § 208 bleibt unberührt.</div></div></div></div></div>
"""

def test_parse_subsub_paragraph_norm():
    BGB_207_DIV = html.fromstring(HTML_BGB_207)
    result = extract_from_div(BGB_207_DIV)

    lens = [0, 2, 0, 0, 0]
    subs = result["paragraphs"][0]["sub"]

    assert 5 == len(subs)
    assert lens == [len(sub["sub"]) for sub in subs]


HTML_BGB_308 = """
<div class="jnnorm" id="BJNR001950896BJNE260205360" title="Einzelnorm"><div class="jnheader"> <a name="BJNR001950896BJNE260205360"></a><a href="index.html#BJNR001950896BJNE260205360">Nichtamtliches Inhaltsverzeichnis</a><h3><span class="jnenbez">§ 308</span>&nbsp;<span class="jnentitel">Klauselverbote mit Wertungsmöglichkeit</span></h3> </div>
<div><div class="jnhtml"><div><div class="jurAbsatz">In Allgemeinen Geschäftsbedingungen ist insbesondere unwirksam <dl style="font-weight:normal;font-style:normal;text-decoration:none;"><dt>1.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Annahme- und Leistungsfrist)</div><div>eine Bestimmung, durch die sich der Verwender unangemessen lange oder nicht hinreichend bestimmte Fristen für die Annahme oder Ablehnung eines Angebots oder die Erbringung einer Leistung vorbehält; ausgenommen hiervon ist der Vorbehalt, erst nach Ablauf der Widerrufsfrist nach § 355 Absatz 1 und 2 zu leisten;</div></dd><dt>1a.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Zahlungsfrist)</div><div>eine Bestimmung, durch die sich der Verwender eine unangemessen lange Zeit für die Erfüllung einer Entgeltforderung des Vertragspartners vorbehält; ist der Verwender kein Verbraucher, ist im Zweifel anzunehmen, dass eine Zeit von mehr als 30 Tagen nach Empfang der Gegenleistung oder, wenn dem Schuldner nach Empfang der Gegenleistung eine Rechnung oder gleichwertige Zahlungsaufstellung zugeht, von mehr als 30 Tagen nach Zugang dieser Rechnung oder Zahlungsaufstellung unangemessen lang ist;</div></dd><dt>1b.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Überprüfungs- und Abnahmefrist)</div><div>eine Bestimmung, durch die sich der Verwender vorbehält, eine Entgeltforderung des Vertragspartners erst nach unangemessen langer Zeit für die Überprüfung oder Abnahme der Gegenleistung zu erfüllen; ist der Verwender kein Verbraucher, ist im Zweifel anzunehmen, dass eine Zeit von mehr als 15 Tagen nach Empfang der Gegenleistung unangemessen lang ist;</div></dd><dt>2.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Nachfrist)</div><div>eine Bestimmung, durch die sich der Verwender für die von ihm zu bewirkende Leistung abweichend von Rechtsvorschriften eine unangemessen lange oder nicht hinreichend bestimmte Nachfrist vorbehält;</div></dd><dt>3.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Rücktrittsvorbehalt)</div><div>die Vereinbarung eines Rechts des Verwenders, sich ohne sachlich gerechtfertigten und im Vertrag angegebenen Grund von seiner Leistungspflicht zu lösen; dies gilt nicht für Dauerschuldverhältnisse;</div></dd><dt>4.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Änderungsvorbehalt)</div><div>die Vereinbarung eines Rechts des Verwenders, die versprochene Leistung zu ändern oder von ihr abzuweichen, wenn nicht die Vereinbarung der Änderung oder Abweichung unter Berücksichtigung der Interessen des Verwenders für den anderen Vertragsteil zumutbar ist;</div></dd><dt>5.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Fingierte Erklärungen)</div><div>eine Bestimmung, wonach eine Erklärung des Vertragspartners des Verwenders bei Vornahme oder Unterlassung einer bestimmten Handlung als von ihm abgegeben oder nicht abgegeben gilt, es sei denn, dass<dl style="font-weight:normal;font-style:normal;text-decoration:none;"><dt>a)</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>dem Vertragspartner eine angemessene Frist zur Abgabe einer ausdrücklichen Erklärung eingeräumt ist und</div></dd><dt>b)</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>der Verwender sich verpflichtet, den Vertragspartner bei Beginn der Frist auf die vorgesehene Bedeutung seines Verhaltens besonders hinzuweisen;</div></dd></dl></div></dd><dt>6.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Fiktion des Zugangs)</div><div>eine Bestimmung, die vorsieht, dass eine Erklärung des Verwenders von besonderer Bedeutung dem anderen Vertragsteil als zugegangen gilt;</div></dd><dt>7.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Abwicklung von Verträgen)</div><div>eine Bestimmung, nach der der Verwender für den Fall, dass eine Vertragspartei vom Vertrag zurücktritt oder den Vertrag kündigt,<dl style="font-weight:normal;font-style:normal;text-decoration:none;"><dt>a)</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>eine unangemessen hohe Vergütung für die Nutzung oder den Gebrauch einer Sache oder eines Rechts oder für erbrachte Leistungen oder</div></dd><dt>b)</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>einen unangemessen hohen Ersatz von Aufwendungen verlangen kann;</div></dd></dl></div></dd><dt>8.</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>(Nichtverfügbarkeit der Leistung)</div><div>die nach Nummer 3 zulässige Vereinbarung eines Vorbehalts des Verwenders, sich von der Verpflichtung zur Erfüllung des Vertrags bei Nichtverfügbarkeit der Leistung zu lösen, wenn sich der Verwender nicht verpflichtet,<dl style="font-weight:normal;font-style:normal;text-decoration:none;"><dt>a)</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>den Vertragspartner unverzüglich über die Nichtverfügbarkeit zu informieren und</div></dd><dt>b)</dt><dd style="font-weight:normal;font-style:normal;text-decoration:none;"><div>Gegenleistungen des Vertragspartners unverzüglich zu erstatten.</div></dd></dl></div></dd></dl></div></div></div></div><div class="jnfussnote" id="BJNR001950896BJNE260205360_FNS"><h4>Fußnote</h4><div><div class="jnhtml"><div><div class="jurAbsatz">(+++ § 308: Zur Anwendung vgl. § 34 BGBEG +++)</div></div></div></div></div></div>
"""

def test_very_complex_norm():
    BGB_308_DIV = html.fromstring(HTML_BGB_308)
    result = extract_from_div(BGB_308_DIV)

    subs = result["paragraphs"][0]["sub"]

    assert 10 == len(subs)
    assert 2 == len(subs[6]["sub"])
    assert 2 == len(subs[8]["sub"])
    assert 2 == len(subs[9]["sub"])
