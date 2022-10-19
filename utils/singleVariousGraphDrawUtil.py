from matplotlib import pyplot as plt


def draw_pie_chart_by_value_and_label(labels, values):
    income_label = 'village', 'city'
    explode = (0, 0)
    plt.pie(values, explode=explode, labels=income_label, autopct='%1.1f%%',
            shadow=False, startangle=90)
    plt.axis('equal')