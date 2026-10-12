def calculate_health(download, upload, ping, packet_loss,
                     jitter, bandwidth, devices):

    score = 100

    # Download Speed
    if download < 20:
        score -= 25
    elif download < 50:
        score -= 10

    # Upload Speed
    if upload < 10:
        score -= 15

    # Ping
    if ping > 100:
        score -= 20
    elif ping > 50:
        score -= 10

    # Packet Loss
    score -= packet_loss * 5

    # Jitter
    if jitter > 30:
        score -= 10

    # Bandwidth
    if bandwidth < 5:
        score -= 10

    # Connected Devices
    if devices > 20:
        score -= 10

    return max(0, min(100, int(score)))

def predict_status(score):

    if score >= 90:
        return "🟢 Excellent"

    elif score >= 75:
        return "🟡 Good"

    elif score >= 60:
        return "🟠 Warning"

    else:
        return "🔴 Critical"