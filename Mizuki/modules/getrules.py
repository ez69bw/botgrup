import random

from telegram import Update
from telegram.ext import CallbackContext, run_async

import Mizuki.modules.getrules_string as getrules_string
from Mizuki import dispatcher
from Mizuki.modules.disable import DisableAbleCommandHandler


@run_async
def rules(update: Update, context: CallbackContext):
    context.args
    update.effective_message.reply_text(random.choice(getrules_string.RULES))


RULES_HANDLER = DisableAbleCommandHandler("rules", rules)


dispatcher.add_handler(RULES_HANDLER)
