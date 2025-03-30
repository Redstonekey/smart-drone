# Smart Drone Documentation

## Initialization:
```python
drone = drone(name: float, hover_speed: float)
```

## Basic Operations

1. **Arming**
```python
drone.arm()
```
- Sets initial hover speed
- Updates starting position
- Enables drone for flight

2. **Disarming**
```python
drone.disarm()
```
- Safety checks (must be landed)
- Stops all motors
- Prevents accidental operation

5. **Taking off**
```python
drone.take_off(hight)
```
- pass hight as float
- Requires armed status check
- Moves drone to specified height
- Maintains hover speed at altitude

4. **Landing**
```python
drone.land()
```
- Gradual descent control
- Ground distance monitoring
- Safe landing sequence


## Usage Example

```python
from drone.drone import drone

# Initialize drone with name and hover speed
drone = drone('drone1', 5)

# Basic flight sequence
drone.arm()
drone.take_off()  # Default height: 5m
drone.land()
drone.disarm()
```

## English version of the idea

### Idea

The Smart Drone project aims to enhance security in various situations, such as during nighttime or in cases of ATM robberies ("Bankautomatensprängung"). The goal is to protect victims by deploying an autonomous drone that responds to emergency calls.

### How It Works

1. **Emergency Activation**: The victim or the ATM triggers a distress call e.g. through an app on phones or smartwatches.
2. **Drone Deployment**: A drone autonomously flies to the victim's location while simultaneously notifying the nearest police station with real-time coordinates.
3. **Incident Assessment**: Upon arrival, a live video feed is manually reviewed by a supervisor to confirm whether it was a false alarm or a real emergency.
4. **Threat Evaluation**: If a weapon is detected, the drone discreetly backs off to avoid alerting the attacker, ensuring the victim's safety. The police receive this critical information immediately.
5. **Tracking the Attacker**: If the attacker flees by car, the drone follows the vehicle, continuously reporting its coordinates to law enforcement. This feature is particularly useful for tracking ATM robbers attempting to escape.

### Proof of Concept

This concept is currently in the proof-of-concept stage.

## Deutsche Version der Idee

Das Smart-Drone-Projekt soll die Sicherheit in verschiedenen Situationen verbessern, beispielsweise in dunklen Nächten oder bei Bankautomatensprengungen. Ziel ist es, Opfer zu schützen, indem eine autonome Drohne auf Notrufe reagiert.

### Funktionsweise

1. **Notruf-Auslösung**: Das Opfer oder der Geldautomat sendet einen Notruf über eine App auf Smartphones oder Smartwatches.
2. **Drohneneinsatz**: Eine Drohne fliegt automatisch zum Opfer und benachrichtigt gleichzeitig die nächstgelegene Polizeidienststelle mit den Echtzeit-Koordinaten.
3. **Vorfallbewertung**: Nach Ankunft wird der Live-Video-Feed von einem Supervisor manuell überprüft, um festzustellen, ob es sich um einen Fehlalarm oder einen echten Notfall handelt.
4. **Bedrohungsanalyse**: Falls eine Waffe erkannt wird, zieht sich die Drohne unauffällig zurück, um den Angreifer nicht zu warnen und die Sicherheit des Opfers zu gewährleisten. Die Polizei erhält diese wichtigen Informationen sofort.
5. **Verfolgung des Angreifers**: Falls der Angreifer mit einem Fahrzeug flieht, verfolgt die Drohne das Auto und sendet kontinuierlich die Koordinaten an die Polizei. Dies ist besonders hilfreich bei der Verfolgung von Bankautomatendieben.

### Proof of Concept

Dies ist aktuell nur ein Konzept.

---


