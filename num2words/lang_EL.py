""""""

from __future__ import division, print_function, unicode_literals

# from . import lang_EU
from num2words import lang_EU

class Num2Word_EL(lang_EU.Num2Word_EU):

    def set_high_numwords(self, high):
        max = 3 + 3 * len(high)
        for word, n in zip(high, range(max, 3, -3)):
            self.cards[10 ** n] = word + "illion"

    def setup(self):
        super(Num2Word_EL, self).setup()

        self.negword = "minus "
        self.pointword = "και"
        self.exclude_title = ["και", "κόμμα", "μείον"]

        self.mid_numwords = [(1000, "χίλια"), (100, "εκατό"),
                             (90, "ενενήντα"), (80, "ογδόντα"), (70, "εβδομήντα"),
                             (60, "εξήντα"), (50, "πενήντα"), (40, "σαράντα"),
                             (30, "τριάντα")]
        self.low_numwords = ["είκοσι", "δεκαεννέα", "δεκαοκτώ", "δεκαεπτά",
                             "δεκαέξι", "δεκαπέντε", "δεκατέσσερα", "δεκατρία",
                             "δώδεκα", "έντεκα", "δέκα", "εννέα", "οκτώ",
                             "επτά", "έξι", "πέντε", "τέσσερα", "τρία", "δύο",
                             "ένα", "μηδέν"]
        self.ords = {"ένα": "πρώτο",  # todo: add genders
                     "δύο": "δεύτερο",
                     "τρία": "τρίτο",
                     "τέσσερα": "τέταρτο",
                     "πέντε": "fifth",
                     "έξι": "sixth",
                     "επτά": "έβδομο",
                     "οκτώ": "όγδοο",
                     "εννέα": "ένατο",
                     "δέκα": "δέκατο",
                     "έντεκα": "ενδέκατο",
                     "δώδεκα": "δωδέκατο"}

        self.CURRENCY_FORMS['EUR'] = (('euro', 'ευρώ'), ('λεπτό', 'λεπτά'))

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        if lnum == 1 and rnum < 100:
            return (rtext, rnum)
        elif 100 > lnum > rnum:
            return ("%s %s" % (ltext, rtext), lnum + rnum)
        elif lnum >= 100 > rnum:
            return ("%s και %s" % (ltext, rtext), lnum + rnum)
        elif rnum > lnum:
            return ("%s %s" % (ltext, rtext), lnum * rnum)
        return ("%s, %s" % (ltext, rtext), lnum + rnum)

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value).split(" ")
        lastwords = outwords[-1].split("-")
        lastword = lastwords[-1].lower()
        try:
            lastword = self.ords[lastword]
        except KeyError:  # todo: ογδοηκοστο δευτερο
            if lastword[-1] == "y":
                lastword = lastword[:-1] + "ie"
            lastword += "th"
        lastwords[-1] = self.title(lastword)
        outwords[-1] = "-".join(lastwords)
        return " ".join(outwords)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return "%s%s" % (value, self.to_ordinal(value)[-2:])

    def to_currency(self, val, currency='EUR', cents=True, separator=' και',
                    adjective=False):
        result = super(Num2Word_EL, self).to_currency(
            val, currency=currency, cents=cents, separator=separator,
            adjective=adjective)
        return result

    def to_year(self, val, suffix=None, longval=True):
        if val < 0:
            val = abs(val)
            suffix = 'BC' if not suffix else suffix
        high, low = (val // 100, val % 100)
        # If year is 00XX, X00X, or beyond 9999, go cardinal.
        if (high == 0
                or (high % 10 == 0 and low < 10)
                or high >= 100):
            valtext = self.to_cardinal(val)
        else:
            hightext = self.to_cardinal(high)
            if low == 0:
                lowtext = "hundred"
            elif low < 10:
                lowtext = "oh-%s" % self.to_cardinal(low)
            else:
                lowtext = self.to_cardinal(low)
            valtext = "%s %s" % (hightext, lowtext)
        return (valtext if not suffix
                else "%s %s" % (valtext, suffix))


def main():
    from num2words import num2words
    print(num2words(92.2, lang='el', ordinal=False, to='currency'))


if __name__ == '__main__':
    main()
