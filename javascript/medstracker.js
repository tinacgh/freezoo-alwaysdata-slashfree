var data = {
    // keys are Sundays
    // morning, evening etc.
    "1 abr 2012": {"1x 10mg olanzapina": "Mo Tu Th Fr Sa Su",
                   "1/2x 10mg olanzapina": "We",
                   "4x 450mg lithium": "Mo Tu We Th Fr Sa Su",
                   "2x 100mg lamotrigina": "Mo Tu We Th Fr Sa Su"
    },
    "22 abr 2012": {"1x 10mg olanzapina": "Mo Tu Th Fr Su",
                    "1/2x 10mg olanzapina": "We Sa",
                    "4x 450mg lithium": "Mo Tu We Th Fr Sa Su",
                    "2x 100mg lamotrigina": "Mo Tu We Th Fr Sa Su"
    },
    "6 mai 2012": {"1x 10mg olanzapina": "Tu Th Sa Su",
                   "1/2x 10mg olanzapina": "Mo We Fr",
                   "4x 450mg lithium": "Mo Tu We Th Fr Sa Su",
                   "2x 100mg lamotrigina": "Mo Tu We Th Fr Sa Su"
    },  

    "15 jul 2012": {"1x 450mg lithium": "Mo We Fr",
                    "1/2x 450mg lithium": "Su Tu Th Sa",
                    "1/2x 10mg olanzapina": "Su Mo Tu We Th",
                    "1/4x 10mg olanzapina": "Fr Sa"
    },

    "22 jul 2012": {"1x 450mg lithium": "We",
                    "1/2x 450mg lithium": "Su Mo Tu Th Fr Sa",
                    "1/2x 10mg olanzapina": "Su Mo We Th",
                    "1/4x 10mg olanzapina": "Tu Fr"
    },

    "19 aug 2012": {"1x 450 lithium": "Su Mo Tu We Th Fr Sa",
                    "1/2x 10mg olanzapina": "Su Mo Tu We Th Fr Sa"
    },

    "2 sep 2012": {"1/4x 450 lithium": "Su Mo Tu We Th Fr Sa",
                   "1/4x 10mg olanzapina": "Su Mo Tu We Th Fr Sa"
    }
};

var weekdays = ["Su","Mo","Tu","We","Th","Fr","Sa"];

var week = {};

var output = '<table><tr><td>Week start</td>';

for (var i = 0, n = weekdays.length; i < n; i++) {
    week[weekdays[i]] = "";
    output += "<td><b>" + weekdays[i] + "</b></td>";
}

output += "</tr>";


for (weekStart in data) {
    output += "<tr>";
    for (var i = 0, n = weekdays.length; i < n; i++) {
        week[weekdays[i]] = "";
    }
    pills = data[weekStart];
    for (pill in pills) {
        var weekdaysToTake = pills[pill].split(" ");
        for (var i = 0, n = weekdaysToTake.length; i < n; i++) {
            week[weekdaysToTake[i]] += pill + "<br>";
        }
    }

    output += "<td><b>" + weekStart + "</b></td>";
    for (var i = 0, n = weekdays.length; i < n; i++) {
        output += "<td>" + week[weekdays[i]] + "</td>";
    }
    output += "</tr>";
}

$("body").append(output);
