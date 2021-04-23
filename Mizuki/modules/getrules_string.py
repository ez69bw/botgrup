RULES = (
            "Kalo tulisannya kotak-kotak adudu, klik aja yang ada dibawah.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Rules", url=f"t.me/{bot.username}?start={chat_id}"
                        ),
                    ],
                ]
            ),
        )