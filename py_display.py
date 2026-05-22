import re
from py_display_colors import Colors as CLR
from py_unicode_char import unicode_char_tupple

c_h_a_r = unicode_char_tupple

qry = """
SELECT COALESCE(`fdr_fdr`.`FDRAmount`, 0) AS `fdr_amount`, (SELECT SUM(CASE WHEN (U0.`Sector` = INT) 
THEN U0.`Credit` ELSE 0 END) AS `interest_during_year` FROM `fdr_fdrledger` U0 WHERE (U0.`FDR_id` = (`fdr_fdr`.`id`) AND NOT U0.`IsArchive`) GROUP BY U0.`FDR_id`) AS `interest_during_year`, (SELECT SUM(CASE WHEN (U0.`Sector` = TAX) THEN U0.`Debit` ELSE 0 END) AS `income_tax_at_source` FROM `fdr_fdrledger` U0 WHERE (U0.`FDR_id` = (`fdr_fdr`.`id`) AND NOT U0.`IsArchive`) GROUP BY U0.`FDR_id`) AS `income_tax_at_source`, (SELECT SUM(CASE WHEN (U0.`Sector` = BAN) THEN U0.`Debit` ELSE 0 END) AS `bank_charge` FROM `fdr_fdrledger` U0 WHERE (U0.`FDR_id` = (`fdr_fdr`.`id`) AND NOT U0.`IsArchive`) GROUP BY U0.`FDR_id`) AS `bank_charge`, (SELECT SUM(CASE WHEN (NOT (U0.`Sector` = INT) AND NOT (U0.`Sector` = BAN) AND NOT (U0.`Sector` = TAX)) THEN U0.`Debit` ELSE 0 END) AS `other_deduction` FROM `fdr_fdrledger` U0 WHERE (U0.`FDR_id` = (`fdr_fdr`.`id`) AND NOT U0.`IsArchive`) GROUP BY U0.`FDR_id`) AS `other_deduction`, (SELECT COALESCE(SUM((COALESCE(U0.`Credit`, 0) - COALESCE(U0.`Debit`, 0))), 0) AS `net_interest` FROM `fdr_fdrledger` U0 WHERE (U0.`FDR_id` = (`fdr_fdr`.`id`) AND NOT U0.`IsArchive`) GROUP BY U0.`FDR_id`) AS `net_interest`, (SELECT COALESCE(U0.`BalanceOnMatureDate`, 0) AS `balance_on_mature_date` FROM `fdr_fdrrenewal` U0 WHERE (U0.`FDR_id` = (`fdr_fdr`.`id`) AND NOT U0.`IsArchive`)) AS `amount_before_maturity`, ((SELECT COALESCE(U0.`BalanceOnMatureDate`, 0) AS `balance_on_mature_date` FROM `fdr_fdrrenewal` U0 WHERE (U0.`FDR_id` = (`fdr_fdr`.`id`) AND Dates = 2024-02-31 AND NOT U0.`IsArchive`)) + (SELECT COALESCE(SUM((COALESCE(U0.`Credit`, 0) - COALESCE(U0.`Debit`, 0))), 0) AS `net_interest` FROM `fdr_fdrledger` U0 WHERE (U0.`FDR_id` = (`fdr_fdr`.`id`) AND NOT U0.`IsArchive`) GROUP BY U0.`FDR_id`)) AS `matured_amount` FROM `fdr_fdr` INNER JOIN `fdr_bankbranch` ON (`fdr_fdr`.`FDRBank_id` = `fdr_bankbranch`.`id`) WHERE (NOT `fdr_fdr`.`IsArchive` AND `fdr_fdr`.`id` = 22) ORDER BY `fdr_bankbranch`.`Bank_id` ASC, `fdr_fdr`.`FDRBank_id` ASC, `fdr_fdr`.`id` ASC;
"""
replacements = [
    (r'INT)', f'{chr(39)}INT{chr(39)})'),
    (r'TAX)', f'{chr(39)}TAX{chr(39)})'), 
    (r'BAN)', f'{chr(39)}BAN{chr(39)})'),
    (r'PAR)', f'{chr(39)}PAR{chr(39)})'),
    (r'VAT)', f'{chr(39)}VAT{chr(39)})'),
    (r'SER)', f'{chr(39)}SER{chr(39)})'),
    (r'FIN)', f'{chr(39)}FIN{chr(39)})'),
    (r'OTH)', f'{chr(39)}OTH{chr(39)})'),
    (r'NEW)', f'{chr(39)}NEW{chr(39)})'),
    (r'(\d{4}-\d{2}-\d{2})', r"'\1'")
]

# Function to replace patterns in a string
def replace_patterns(text, replacements):
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text


# result = replace_patterns(text, replacements)
def display(text, query=False, mysql=False, leading_text="Returned Data 📋", text_clr=CLR.Fg.red, border=True, border_char=c_h_a_r[1489][1]):
    if border:
        print((f"*").join(border_char*20))
    
    #! main Text to print ======
    print(f'\033[38;5;208m {CLR.Bg.cyan}{CLR.bold}\033[2:4m {leading_text}{CLR.reset} {text_clr} {text}{CLR.reset}')
    
    # if border:
    #     print(("=").join(border_char*15))
        
    if query:
        query_result_txt = f'\033[38;5;208m {CLR.Bg.magenta}{CLR.bold} Query 📋:{CLR.reset} \033[2;30m\
{str(text.query).replace(chr(34), "`")};\n\
{c_h_a_r[884][1]} Total Number of Records: {CLR.Fg.green}{CLR.bold}{text.count()}{CLR.reset}'

        if mysql:
            query_result_txt=f'{query_result_txt.replace("CAST(","").replace("AS NUMERIC)","")}\n\
{c_h_a_r[884][1]} Total Number of Records: {CLR.Fg.green}{CLR.bold}{text.count()}{CLR.reset}'
        # query_result = re.sub(r'(\d{4}-\d{2}-\d{2})', r"'\1'", query_result_txt)
        query_result = replace_patterns(query_result_txt,replacements)
        print(query_result)
        print((f" {c_h_a_r[1491][1]} ").join(c_h_a_r[1496][1]*15),"\n")
        
def run():
    display(text="Test Text", query=False, mysql=False, leading_text="Returned Data 📋", text_clr=CLR.Fg.red, border=True, border_char="~")


if __name__ == "__main__":
    run()
    
#! TODO: Change `BETWEEN YYYY-mm-dd AND YYYY-mm-dd` with `BETWEEN "YYYY-mm-dd" AND "YYYY-mm-dd"`
# BETWEEN "2024-09-01" AND "2024-09-21"
# To replace a date range in the format `BETWEEN YYYY-mm-dd AND YYYY-mm-dd` 
# with `BETWEEN "YYYY-mm-dd" AND "YYYY-mm-dd"` in Python, 
# you can use the `re` module for regular expressions. Here's an example:

#! FIXME: Code ====================
# import re
# date_range_str = "BETWEEN 2024-09-01 AND 2024-09-21"
# formatted_date_range_str = re.sub(r'(\d{4}-\d{2}-\d{2})', r'"\1"', date_range_str)
# print(formatted_date_range_str)
#! FIXME: Code End ================
# ```
# This code will output:
# ```
# BETWEEN "2024-09-01" AND "2024-09-21"
# ```
"""
The `re.sub` function is used here to find all occurrences of the date pattern `YYYY-mm-dd` 
and replace them with `"YYYY-mm-dd"`.
"""
