def process_input(file_data=None):
    data = [
        "Writing Fast Tests Against Enterprise Rails 60min",
        "Overdoing it in Python 45min",
        "Lua for the Masses 30min",
        "Ruby Errors from Mismatched Gem Versions 45min",
        "Common Ruby Errors 45min",
        "Rails for Python Developers lightning",
        "Communicating Over Distance 60min",
        "Accounting-Driven Development 45min",
        "Woah 30min",
        "Sit Down and Write 30min",
        "Pair Programming vs Noise 45min",
        "Rails Magic 60min",
        "Ruby on Rails: Why We Should Move On 60min",
        "Clojure Ate Scala (on my project) 45min",
        "Programming in the Boondocks of Seattle 30min",
        "Ruby vs. Clojure for Back-End Development 30min",
        "Ruby on Rails Legacy App Maintenance 60min",
        "A World Without HackerNews 30min",
        "User Interface CSS in Rails Apps 30min"
    ]

    if file_data:
        data = file_data

    lightning_duration = 5
    talks = []
    total_talks_duration = 0

    for line in data:
        line_pieces = line.split(' ')
        lightning = True
        duration = 0
        for piece in line_pieces:
            if piece[0].isdigit():
                min_index = piece.find('min')
                if min_index > -1:  # unnecessary, but we never know
                    duration = int(piece[:min_index])
                    lightning = False

        if lightning:
            talk_title = line[:-len('lightning')].strip()
            talks.append((talk_title, lightning_duration,))  # (title, duration, starting_time)
            total_talks_duration += lightning_duration
        else:
            talk_title = line[:line.find(str(duration))].strip()
            talks.append((talk_title, duration,))  # (title, duration, starting_time)
            total_talks_duration += duration

    return talks, total_talks_duration


def organize_talks(talks, total_duration):
    morning_duration = 180  # 3h
    afternoon_duration = 240  # 4h
    track_duration = morning_duration + afternoon_duration  # 420 - 7h

    morning_start_time = 540  # 9AM
    afternoon_start_time = 60  # 1PM

    from math import ceil
    num_tracks = ceil(float(total_duration) / float(track_duration))

    morning_counter = 0
    afternoon_counter = 0

    # group talks by duration
    grouped_talks = {}
    for talk in talks:
        if talk[1] in grouped_talks:
            grouped_talks[talk[1]].append(talk)
        else:
            grouped_talks[talk[1]] = [talk]

    schedule = {}
    filled_tracks = 0
    morning_talks = []
    afternoon_talks = []

    while filled_tracks < num_tracks:
        for talk in talks:
            if talk[1] in grouped_talks and talk in grouped_talks[talk[1]]:
                if morning_duration - morning_counter >= talk[1]:
                    grouped_talks[talk[1]].remove(talk)
                    if len(grouped_talks[talk[1]]) == 0:
                        grouped_talks.pop(talk[1], None)

                    talk = (talk[0], talk[1], morning_start_time + morning_counter)
                    morning_talks.append(talk)
                    morning_counter += talk[1]
                elif afternoon_duration - afternoon_counter >= talk[1]:
                    grouped_talks[talk[1]].remove(talk)
                    if len(grouped_talks[talk[1]]) == 0:
                        grouped_talks.pop(talk[1], None)

                    talk = (talk[0], talk[1], afternoon_start_time + afternoon_counter)
                    afternoon_talks.append(talk)
                    afternoon_counter += talk[1]

        if len(grouped_talks.keys()) > 0:
            shortest_duration = min(grouped_talks.keys())
        else:
            shortest_duration = 0

        if (morning_counter == morning_duration and afternoon_counter == afternoon_duration) or \
                (morning_counter + shortest_duration > morning_duration and afternoon_counter + shortest_duration > afternoon_duration) or \
                shortest_duration == 0:
            filled_tracks += 1
            schedule[filled_tracks] = [morning_talks, afternoon_talks]
            morning_talks, afternoon_talks = [], []
            morning_counter, afternoon_counter = 0, 0

    return schedule


def print_schedule(schedule):
    from math import modf

    for track, sessions in schedule.items():
        print("Track {}:".format(track))
        morning_sessions = sessions[0]
        afternoon_sessions = sessions[1]

        for talk in morning_sessions:
            temp_time = float(talk[2]) / 60.0
            if temp_time.is_integer():
                start_time = "%02d:00" % (int(temp_time),)
            else:
                split_time = modf(temp_time)
                start_time = "%02d:%02d" % (int(split_time[1]), int(split_time[0] * 60))

            title = talk[0]
            duration = str(talk[1])
            if duration == '5':
                duration = 'lightning'
            else:
                duration += 'min'
            print("{}AM {} {}".format(start_time, title, duration))

        print("12:00PM Lunch")

        for talk in afternoon_sessions:
            temp_time = float(talk[2]) / 60.0
            if temp_time.is_integer():
                start_time = "%02d:00" % (int(temp_time),)
            else:
                split_time = modf(temp_time)
                start_time = "%02d:%02d" % (int(split_time[1]), int(split_time[0] * 60))

            title = talk[0]
            duration = str(talk[1])
            if duration == '5':
                duration = 'lightning'
            else:
                duration += 'min'
            print("{}PM {} {}".format(start_time, title, duration))

        print("05:00PM Networking Event")


def main(file_contents=None):
    if file_contents:
        talks, total_talks_duration = process_input(file_contents)
    else:
        talks, total_talks_duration = process_input()
    talks_by_duration = sorted(talks, key=lambda x: x[1], reverse=True)
    schedule = organize_talks(talks_by_duration, total_talks_duration)
    print_schedule(schedule)

if __name__ == '__main__':
    import sys

    filename = sys.argv[-1]
    if filename != sys.argv[0]:
        with open(filename) as f:
            content = f.readlines()
            main(content)
    else:
        print("You must pass a file as a command-line argument or "
              "I'll use hardcoded data instead.")
        main()
