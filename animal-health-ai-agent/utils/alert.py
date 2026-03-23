def check_alert(risk_score, threshold=0.7):
    if risk_score > threshold:
        return {
            "alert": True,
            "message": f"⚠️ High Risk Alert! Score: {risk_score}"
        }
    return {"alert": False}