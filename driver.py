from client import Client
import math

# ================= Parameters (Optimized with IBM Granite) =================
TARGET_SPEED = 290
STEER_GAIN = 32
CENTERING_GAIN = 0.6

# ================= Control Modules =================

def calculate_steering(S):
    target_pos = 0.0
    if S['angle'] > 0.05: target_pos = 0.3
    elif S['angle'] < -0.05: target_pos = -0.3
    
    force_correction = 0.0
    if abs(S['trackPos']) > 0.8:
        target_pos = 0.0
        force_correction = S['trackPos'] * 0.8
    
    steer = (S['angle'] * STEER_GAIN / math.pi) - ((S['trackPos'] - target_pos) * CENTERING_GAIN) - force_correction
    if S['speedX'] > 200: steer *= 0.6
    return max(-1, min(1, steer))

def calculate_throttle_and_brake(S, R):
    vision_dist = max(S['track'][8:11])
    current_speed = S['speedX']
    
    # Target speed logic
    if vision_dist > 80: current_target = 300
    elif vision_dist < 35: current_target = 75
    else: current_target = 170

    # Braking logic
    brake = 0.0
    if current_speed > 85:
        if vision_dist < 75 and current_speed > 140: brake = 0.5
        if vision_dist < 20: brake = 1.0

    # Throttle logic
    accel = 1.0 if current_speed < current_target else 0.0
    if abs(R['steer']) > 0.3: accel = min(accel, 0.5)
    
    return accel, brake

def shift_gears(S, R):
    rpm = S['rpm']
    gear = R['gear']
    if rpm > 9200 and gear < 6: return gear + 1
    if rpm < 3800 and gear > 1: return gear - 1
    return gear

# ================= Main Loop =================

def drive(c):
    S, R = c.S.d, c.R.d
    R['steer'] = calculate_steering(S)
    R['accel'], R['brake'] = calculate_throttle_and_brake(S, R)
    R['gear'] = shift_gears(S, R)

if __name__ == "__main__":
    C = Client(p=3001)
    print("AI Driver connected. Starting race...")
    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        drive(C)
        C.respond_to_server()
    C.shutdown()
