import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import os
import math
import matplotlib.patches as mpatches

x_axis_age = []
diagnosis_to_axis_map = []

def hover(event):
    vis = annot.get_visible()

    if event.inaxes != ax:
        return

    cont, ind = sc.contains(event)

    if cont:
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        y_index = math.floor(event.ydata)

        if y_index < 0:
            y_index = 0

        disease = [a[0] for a in  diagnosis_to_axis_map.items() if a[1] == y_index][0]
        age = math.ceil(event.xdata) #x_axis_age[math.ceil(event.xdata)]

        text = f'Age: {age} \nDisease: {disease}'
        annot.set_text(text)
        #annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_facecolor('white')
        annot.get_bbox_patch().set_alpha(0.9)
        annot.set_visible(True)
        fig.canvas.draw_idle()
    else:
        if vis:
            annot.set_visible(False)
            fig.canvas.draw_idle()

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'openmrs.db')
    print(db_path)
    print(os.getcwd())
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT diagnosis.name as diagnosis_name, patient.gender as gender, (date('now') - patient.birthdate) as age
        FROM diagnosis
        INNER JOIN encounter_diagnosis ON encounter_diagnosis.diagnosis_id =  diagnosis.id
        INNER JOIN encounter ON encounter.id = encounter_diagnosis.encounter_id
        INNER JOIN patient ON patient.id = encounter.patient_id
        ORDER BY diagnosis.name desc
    ''')
    data = cursor.fetchall()
    data_length = len(data)
    diagnosis_to_axis_map = {}
    diagnosis_to_axis_map = {}

    # cannot plot diagnosis name, so need to convert it to a number
    current_diagnosis_number = 0
    for datum in data:
        if datum[0] in diagnosis_to_axis_map:
            continue

        diagnosis_to_axis_map[datum[0]] = current_diagnosis_number
        current_diagnosis_number += 1

    x_axis_age = []
    y_axis_disease = []
    male_color = 'blue'
    female_color = 'pink'
    unspecified_gender_color = 'red'
    color = ''
    color_map = []

    for datum in data:
        disease_diagnosis = datum[0]
        disease_axis = diagnosis_to_axis_map[disease_diagnosis]
        gender = datum[1].upper()
        age = datum[2]

        x_axis_age.append(age)
        y_axis_disease.append(disease_axis)

        if gender == 'M':
            color_map.append(male_color)
            color = male_color
        elif gender == 'F':
            color_map.append(female_color)
            color = female_color
        else:
            color_map.append(unspecified_gender_color)
            color = unspecified_gender_color

    x = x_axis_age #np.random.rand(150)
    y = y_axis_disease #np.random.rand(150)
    c = color_map # np.random.randint(1,5,size=150)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    sc = plt.scatter(x,y,c=c,  alpha=0.9, marker='.', s=10)

    #ax.set_yticklabels(list(diagnosis_to_axis_map.keys()))
    ax.set_yticklabels(['']* data_length)
    ax.set_yticks(range(len(diagnosis_to_axis_map.values())))
    ax.set_title('Diagnosis vs Age, per gender', fontsize=20)
    ax.set_xlabel('Age', fontsize=15)
    ax.set_ylabel('Disease (mouse over)', fontsize=15)
    ax.grid(False)

    # legend
    classes = ['Male','Female','Unspecified']
    class_colours = ['b','pink','r']
    recs = []
    for i in range(0,len(class_colours)):
        recs.append(mpatches.Rectangle((0,0),1,1,fc=class_colours[i]))
    plt.legend(recs,classes,loc=4)

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.show()


finally:
    cursor.close()
    conn.close()
