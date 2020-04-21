
# post_list = soup.select('#react-root > section > main > div > div > article > div > div')

# number = 1
# for post_row in post_list:
#     for post in post_row.select('div > div > a > div > div'):
#         if not post.select('img') == []:
#             # print("image_url :", number, post.select('img')[0])
#             print("image_url :", number, post.select('img')[0].get('src'))
#             number += 1
#     print()
#     print()