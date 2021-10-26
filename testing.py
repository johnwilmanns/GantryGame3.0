# x = 1
# y = 2
# z = 3

# # def axes():
# #     yield x
# #     yield y
# #     yield z

# class axes():
#     def __getitem__(self, key):
#         if key == 0:
#             return x
#         elif key == 1:
#             return y
#         elif key == 2:
#             return z

#     def __iter__(self):
#         yield x
#         yield y
#         yield z

# test = axes()

# print(test[2])

class Item:
    def __iter__(self):
        return IterItem()


class IterItem:
   def __init__(self):
      self.val = 0
   def __iter__(self):
      return self
   def __next__(self):
      if self.val > 2: raise StopIteration
      res = range(0, 30, 10)[self.val]
      self.val += 1
      return res

i = Item()

for j in iter(i):
    print(j)