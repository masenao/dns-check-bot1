from telegram import Update       #Библиотека
from telegram.ext import Application, CommandHandler, ContextTypes  #Библиотека
import dns.resolver             #Библиотека
import os 
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("token")
print(f"Токен: {token[:10]}...")
#Функция /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне домен, и я покажу его записи.")

#Функция /check
async def check_domain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Пример: /check example.com")
        return
    domain = context.args[0]
    result = get_dns_record(domain)
    await update.message.reply_text(f"Проверяю домен {domain} ...")
    await update.message.reply_text(result)

def get_dns_record(domain):
    result = {}
    record_types = ['A', 'AAAA', 'CNAME', 'MX']

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            result[record_type] = [str(r) for r in answers]
        except dns.resolver.NXDOMAIN:
            return f"Домен {domain} не найден."
        except dns.resolver.NoAnswer:
            result[record_type] = []
        except Exception as e:
            result[record_type] = [f"Ошибка: {e}"]

    output = f"DNS-записи для {domain}: \n"
    for record_type, records in result.items():
        if records:
            output += f"{record_type}: {', '.join(records)}\n"
        else:
            output += f"{record_type}: нет записей.\n"
    
    return output

def main():
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_domain))

    print("Бот запущен!")

    app.run_polling()

if __name__ == "__main__":
    main()