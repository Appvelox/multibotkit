from multibotkit.helpers.telegram import TelegramHelper


h = TelegramHelper(token="5354048863:AAHuPvbVGRy1eNAf-GZeBLdmnSzU_q0JQzI")
bf = h.sync_get_file(file_id="AgACAgIAAxkBAAIE1mL_Mprw3isehUxe8LPgCLCdFwFGAAJawTEbWlfwS_6cqJT-901LAQADAgADcwADKQQ")

f = open(bf.name, "rb")
f2 = open("1.jpg", "wb")
for i in f:
    f2.write(i)
f2.close()