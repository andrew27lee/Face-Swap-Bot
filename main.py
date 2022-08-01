import os, cv2, discord
from dotenv import load_dotenv
from discord.ext import commands
from face_detection import select_face, select_all_faces
from face_swap import face_swap

SOURCE_PATH = 'static/images/input/src.jpg'
DESTINATION_PATH = 'static/images/input/dst.jpg'
RESULT_PATH = 'static/images/output/swapped.jpg'

load_dotenv('.env')
bot = commands.Bot(command_prefix='!')


def __image_swap():
    src_img = cv2.imread(SOURCE_PATH)
    dst_img = cv2.imread(DESTINATION_PATH)
    
    try:
        src_points, _, src_face = select_face(src_img)
        dst_faceBoxes = select_all_faces(dst_img)

        if src_points is None or dst_faceBoxes is None:
            return 'No face was detected.'

        output = dst_img

        for k, dst_face in dst_faceBoxes.items():
            output = face_swap(src_face, dst_face["face"], src_points,
                            dst_face["points"], dst_face["shape"],
                            output)

        cv2.imwrite(RESULT_PATH, output)
        return None
    except:
        return "An error has occurred."


@bot.command()
async def faceswap(ctx):
    ctx.message.attachments[0].url.save(os.path.join(SOURCE_PATH))
    ctx.message.attachments[1].url.save(os.path.join(DESTINATION_PATH))
    error = __image_swap()
    
    if error:
        await ctx.reply('An error has occurred. Please try again.')
    await ctx.send(file=discord.File(RESULT_PATH))


bot.run(os.getenv('TOKEN'))
