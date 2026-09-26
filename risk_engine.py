def clamp(x, lo=0, hi=100):
    return max(lo, min(hi, x))

def norm(x, lo, hi):
    return clamp((x-lo)/(hi-lo)*100)

def calculate_risk(wind, rainfall, surge, lead_time):
    wind_score = norm(wind, 60, 240)
    rain_score = norm(rainfall, 20, 600)
    surge_score = norm(surge, 0.2, 6.0)
    lead_score = clamp(100 - norm(lead_time, 6, 72))
    overall = round(0.38*wind_score + 0.27*rain_score + 0.25*surge_score + 0.10*lead_score)

    actions = []
    if overall >= 75:
        actions.append("Activate high-priority emergency coordination.")
    elif overall >= 50:
        actions.append("Increase preparedness and inter-agency monitoring.")
    else:
        actions.append("Continue monitoring and verify incoming data.")
    if surge >= 2.5:
        actions.append("Inspect low-lying coastal roads and evacuation routes.")
    if rainfall >= 250:
        actions.append("Pre-position pumps, rescue teams and medical supplies.")
    if wind >= 130:
        actions.append("Inspect power, telecom and port infrastructure.")
    if lead_time <= 24:
        actions.append("Prioritize time-critical alerts and evacuation decisions.")

    return {"overall_score": overall, "wind_score": round(wind_score),
            "rain_score": round(rain_score), "surge_score": round(surge_score),
            "lead_score": round(lead_score), "actions": actions}
