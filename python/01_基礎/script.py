import matplotlib.pyplot as plt

label = ["A", "B", "C", "D"]
num = [100, 50, 30, 40]

# plt.bar(label, num)
# plt.savefig('./bar.png')

plt.legend(label, num)
plt.savefig('./legend.png')