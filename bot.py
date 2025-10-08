import os
import logging
import sympy as sp
from sympy import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Symbols
x, y, z, t = symbols('x y z t')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    text = """🧮 **Math Solver Bot**

📚 Commands:
/solve x^2+5x+6=0 - Solve equation
/simplify (x+2)*(x+3) - Simplify
/expand (x+1)^3 - Expand
/factor x^2+5x+6 - Factor
/diff x^2+3x - Differentiate
/integrate sin(x) - Integrate
/graph x^2 - Plot graph
/matrix [[1,2],[3,4]] - Matrix info

Just type: x^2+5x+6"""
    
    await update.message.reply_text(text)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def solve_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /solve x^2+5x+6=0")
        return
    
    try:
        text = ' '.join(context.args)
        await update.message.reply_text("⏳ Solving...")
        
        if '=' in text:
            left, right = text.split('=')
            eq = sp.sympify(left) - sp.sympify(right)
        else:
            eq = sp.sympify(text)
        
        sols = sp.solve(eq, x)
        
        if sols:
            result = f"✅ Solutions:\n\n"
            for i, sol in enumerate(sols, 1):
                result += f"{i}. x = {sol}\n"
        else:
            result = "❌ No solution found"
        
        await update.message.reply_text(result)
    except Exception as e:
        logger.error(f"Solve error: {e}")
        await update.message.reply_text("❌ Error. Check format.")

async def simplify_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /simplify (x+2)*(x+3)")
        return
    
    try:
        text = ' '.join(context.args)
        expr = sp.sympify(text)
        result = sp.simplify(expr)
        
        msg = f"✅ Simplified:\n\nInput: {expr}\nOutput: {result}"
        await update.message.reply_text(msg)
    except Exception as e:
        logger.error(f"Simplify error: {e}")
        await update.message.reply_text("❌ Error")

async def expand_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /expand (x+1)^3")
        return
    
    try:
        text = ' '.join(context.args)
        expr = sp.sympify(text)
        result = sp.expand(expr)
        
        msg = f"✅ Expanded:\n\nInput: {expr}\nOutput: {result}"
        await update.message.reply_text(msg)
    except Exception as e:
        logger.error(f"Expand error: {e}")
        await update.message.reply_text("❌ Error")

async def factor_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /factor x^2+5x+6")
        return
    
    try:
        text = ' '.join(context.args)
        expr = sp.sympify(text)
        result = sp.factor(expr)
        
        msg = f"✅ Factored:\n\nInput: {expr}\nOutput: {result}"
        await update.message.reply_text(msg)
    except Exception as e:
        logger.error(f"Factor error: {e}")
        await update.message.reply_text("❌ Error")

async def diff_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /diff x^2+3x")
        return
    
    try:
        text = ' '.join(context.args)
        expr = sp.sympify(text)
        result = sp.diff(expr, x)
        
        msg = f"✅ Derivative:\n\nf(x) = {expr}\nf'(x) = {result}"
        await update.message.reply_text(msg)
    except Exception as e:
        logger.error(f"Diff error: {e}")
        await update.message.reply_text("❌ Error")

async def integrate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /integrate sin(x)")
        return
    
    try:
        text = ' '.join(context.args)
        expr = sp.sympify(text)
        result = sp.integrate(expr, x)
        
        msg = f"✅ Integral:\n\nf(x) = {expr}\n∫f(x)dx = {result} + C"
        await update.message.reply_text(msg)
    except Exception as e:
        logger.error(f"Integrate error: {e}")
        await update.message.reply_text("❌ Error")

async def graph_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /graph x^2")
        return
    
    try:
        text = ' '.join(context.args)
        await update.message.reply_text("⏳ Creating graph...")
        
        expr = sp.sympify(text)
        f = sp.lambdify(x, expr, 'numpy')
        
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, 'b-', linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)
        plt.title(f'f(x) = {expr}', fontsize=14)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        await update.message.reply_photo(photo=buf, caption=f"✅ Graph: f(x) = {expr}")
    except Exception as e:
        logger.error(f"Graph error: {e}")
        await update.message.reply_text("❌ Error creating graph")

async def matrix_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /matrix [[1,2],[3,4]]")
        return
    
    try:
        text = ' '.join(context.args)
        mat = sp.Matrix(eval(text))
        
        msg = f"✅ Matrix:\n\n{mat}\n\n"
        msg += f"Size: {mat.shape[0]}×{mat.shape[1]}\n"
        msg += f"Det: {mat.det()}"
        
        await update.message.reply_text(msg)
    except Exception as e:
        logger.error(f"Matrix error: {e}")
        await update.message.reply_text("❌ Error")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text.startswith('/'):
        return
    
    try:
        expr = sp.sympify(text)
        result = sp.simplify(expr)
        
        msg = f"✅ Simplified:\n\n{text}\n= {result}"
        await update.message.reply_text(msg)
    except:
        pass

def main():
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        raise ValueError("Token not found")
    
    # Build application
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("solve", solve_cmd))
    app.add_handler(CommandHandler("simplify", simplify_cmd))
    app.add_handler(CommandHandler("expand", expand_cmd))
    app.add_handler(CommandHandler("factor", factor_cmd))
    app.add_handler(CommandHandler("diff", diff_cmd))
    app.add_handler(CommandHandler("integrate", integrate_cmd))
    app.add_handler(CommandHandler("graph", graph_cmd))
    app.add_handler(CommandHandler("matrix", matrix_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    logger.info("Bot started!")
    app.run_polling()

if __name__ == '__main__':
    main()
