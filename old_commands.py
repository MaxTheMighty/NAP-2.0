#     #BE VERY CAREFUL WITH THIS
#     @commands.command(is_owner=True,hidden=True)
#     async def think(self,ctx):
#         question = ctx.message.content[7:]
#         question_send = f"""Marv is a chatbot that reluctantly answers questions.\n
# ###
# User: How many pounds are in a kilogram?
# Marv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.
# ###
# User: What does HTML stand for?
# Marv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.
# ###
# User: {question}?
# Marv: """
#         # print(question_send)
#         resp = openai.Completion.create(
#             engine="davinci",
#             prompt=question_send,
#             max_tokens=50,
#             temperature=0.8,
#             top_p=0.7,
#             stop='###'
#         )
#         # print(resp)
#         answer = resp.choices[0]['text']
#         print(answer)
#         try:
#             await ctx.send(answer)
#         except discord.errors.HTTPException:
#             await ctx.send("ERROR: No response")

