# Battlesnake
## Overview
Battlesnake is a multiplayer programming game where each player utilizes snake AI to compete against others. This project uses Python 3 and leverages Flask to receive board state and return game input via a REST API. N-step ahead forecasting is employed to enable the snakes to look ahead multiple permutations and make optimal decisions. As part of the project, two variants of the snake were developed: 1) Multiplayer Battle Snake and 2) Solo Survival Snake.

### Multiplayer Battle Snake
Battle Snake is optimized to operate efficiently while accounting for possible moves of other snakes. It prefers to stay lean and avoid unnecessary risks. Due to the presence of additional snakes and time constraints, it is limited to forecasting only 2 moves ahead.

Observations from the video include:
- Turn 75 shows the snake turning away as getting within a 1-block radius of the snake's next head position carries certain risk.
- This is different from turn 99 when it confidently takes the food, knowing it is in an advantageous position before the enemy snake can make a turn.
- On turn 100, it pivots upward to avoid exploring too closely to the enemy snake.

[Multiplayer Battle Snake Video](https://www.youtube.com/embed/WAP-yWF8-fs?si=nm4KS91c2mV7ac5Z)

### Solo Survival Snake
Solo Survival Snake is optimized to consider greater depth and prioritize food consumption. Increased depth consideration is achieved by focusing solely on the snake itself. The snake is granted more flexibility to consume food due to reduced uncertainty in subsequent turns.

Observations from the video include:
- The food-seeking behavior is more evident compared to the battle-optimized snake from the beginning.
- Turn 156 exemplifies awareness of future steps and a preference for empty space by turning away from the tail.
- After a brief detour, the snake resumes chasing the tail in pursuit of the next food.
- Similar behavior is observed at turn 178.
- Starting from Turn 220, the snake becomes stuck as additional food consumption would lead to its demise.

[Solo Survival Snake Video](https://www.youtube.com/embed/cdetPrKb_zA?si=hidJV6eBD441Z2xW)



## Links
* Platform: [play.battlesnake.com](https://play.battlesnake.com)
* API Documentation: [Battlesnake API Docs](https://docs.battlesnake.com/api)
* Achievements: [Achievements](https://play.battlesnake.com/profile/ericpien#achievements)
