async def progress(current, total, up_msg, message):
    try:
        await message.edit(
            text=f"{up_msg} {current * 100 / total:.1f}%"
        )
    except:
        pass
