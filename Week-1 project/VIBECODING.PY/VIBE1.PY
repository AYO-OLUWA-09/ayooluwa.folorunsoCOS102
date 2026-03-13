import time

def morning_routine():
    steps = [
        ("⏰ Wake up & turn off alarm",   1),
        ("🚿 Brush teeth & take a shower", 2),
        ("👕 Get dressed",                 1),
    ]

    print("=== MORNING ROUTINE ===")
    for step, duration in steps:
        print(f"  {step} (~{duration} min)")

    breakfast_ready = input("\nIs breakfast ready? (yes/no): ").lower()
    if breakfast_ready == 'yes':
        print("  🍳 Eating breakfast...")
    else:
        print("  🥣 Preparing a quick meal...")
        print("  🍳 Eating breakfast...")

    print("  🎒 Packing bag and gathering items...")

    current_time = input("\nCurrent time (e.g. 07:30): ")
    depart_time  = input("Departure time (e.g. 07:45): ")

    if current_time < depart_time:
        print(f"  ⏳ Waiting until {depart_time}...")
    
    print("\n🚪 Leaving house. Have a great day!")

morning_routine()
    