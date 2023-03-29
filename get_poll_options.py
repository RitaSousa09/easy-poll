import holidays
from datetime import date, timedelta

CURRENT_YEAR = date.today().year

TIME_OF_DAY = {
    "afternoon": "14h-17h",
    "evening": "17h-20h",
    "night": "20h-00h"
}

# If needed, insert a question to ask for a different title
poll_title = "Próxima sessão D&D"
# If needed, insert a question to include the holiday and the night before
include_pre_holiday = True
include_holiday = True


def get_poll_date_interval():
    print("\nSet the date range that you want to know the availability of your group.")
    initial_day = int(input("\nSTART date\nDay:\n"))
    initial_month = int(input("Month (1-12):\n"))
    initial_year = int(input("Year (0, if it's the actual):\n"))

    initial_date = date(CURRENT_YEAR if initial_year == 0 else initial_year, initial_month, initial_day)
    if initial_date < date.today():
        print("ERROR! Start date is in the past!")
        exit(1)

    final_day = int(input("\nFINAL date\nDay:\n"))
    final_month = int(input("Month (1-12):\n"))
    final_year = int(input("Year (0, if it's the actual):\n"))

    final_date = date(CURRENT_YEAR if final_year == 0 else final_year, final_month, final_day)

    if final_date < initial_date:
        print("ERROR! Initial date (${initial_date}) must be earlier than final date (${final_date})!")
        exit(1)
    
    return initial_date, final_date


def set_poll_options(poll_template):
    initial_date, final_date = get_poll_date_interval()
    possible_dates = list((initial_date + timedelta(idx)
            for idx in range((final_date - initial_date).days)))

    country_holidays = holidays.Portugal(years = CURRENT_YEAR).items()

    for possible_date in possible_dates:
        if possible_date.weekday() == 4:
            poll_template["poll_options"].append({ "type": "text", "value": possible_date.strftime("%d %b (%a) ") + TIME_OF_DAY["night"] })
        elif possible_date.weekday() == 5 or possible_date.weekday() == 6:
            for day_time in TIME_OF_DAY:
                poll_template["poll_options"].append({ "type": "text", "value": possible_date.strftime("%d %b (%a) ") + TIME_OF_DAY[day_time] })
        elif any(possible_date in holiday for holiday in country_holidays):
            if include_pre_holiday:
                pre_holiday = possible_date - timedelta(days=1)
                poll_template["poll_options"].append({ "type": "text", "value": pre_holiday.strftime("%d %b (%a) ") + TIME_OF_DAY["night"] })
            if include_holiday:
                for day_time in TIME_OF_DAY:
                    poll_template["poll_options"].append({ "type": "text", "value": possible_date.strftime("%d %b (%a) ") + TIME_OF_DAY[day_time] })
    return poll_template


def get_poll_description(poll_template):
    description = input("\nInsert a description with special notes for this session:\n")
    poll_template["poll_meta"]["description"] = description
    poll_template["title"] = poll_title
    return poll_template


def set_personalized_poll(poll_template):
    poll_with_description = get_poll_description(poll_template)
    poll_completed = set_poll_options(poll_with_description)
    return poll_completed
