def analyze_complaint(complaint):
	"""Classify a complaint and summarize its description."""
	description = complaint.get("description", "").strip()
	description_lower = description.lower()
	summary = f"Customer reports: {description}" if description else "No complaint description was provided."

	if "side effect" in description_lower or "adverse reaction" in description_lower:
		category = "Side Effect or Adverse Reaction"
		severity = "Critical"
		priority = "Urgent"

	elif "wrong product" in description_lower or "incorrect product" in description_lower:
		category = "Wrong Product"
		severity = "High"
		priority = "Urgent"

	elif "missing tablet" in description_lower or "missing tablets" in description_lower:
		category = "Missing Tablets"
		severity = "Medium"
		priority = "High"

	elif "packaging" in description_lower or "package" in description_lower:
		category = "Packaging Issue"
		severity = "Medium"
		priority = "Medium"

	elif "quality" in description_lower or "contaminated" in description_lower:
		category = "Quality Issue"
		severity = "High"
		priority = "High"

	elif "damaged" in description_lower or "broken" in description_lower:
		category = "Product Damage"
		severity = "High"
		priority = "High"

	elif "wrong" in description_lower or "incorrect" in description_lower:
		category = "Incorrect Product"
		severity = "Medium"
		priority = "Medium"

	elif "late" in description_lower or "delay" in description_lower:
		category = "Delivery Delay"
		severity = "Medium"
		priority = "High"

	else:
		category = "General Complaint"
		severity = "Low"
		priority = "Low"

	if any(word in description_lower for word in ("storage", "temperature", "heat", "cold", "frozen")):
		root_cause = "Storage issue"
	elif category == "Delivery Delay" or any(word in description_lower for word in ("transport", "shipping", "delivery")):
		root_cause = "Delivery/transport issue"
	elif category in ("Packaging Issue", "Product Damage"):
		root_cause = "Packaging damage"
	elif category in (
		"Side Effect or Adverse Reaction",
		"Wrong Product",
		"Missing Tablets",
		"Quality Issue",
		"Incorrect Product",
	):
		root_cause = "Manufacturing issue"
	else:
		root_cause = "Unknown root cause"

	if category == "Side Effect or Adverse Reaction" or severity == "Critical":
		corrective_action = "Escalate the case to Pharmacovigilance and review or quarantine the affected batch."
		preventive_action = "Monitor safety signals and strengthen adverse-reaction review and reporting."
	elif root_cause == "Storage issue":
		corrective_action = "Check storage conditions, assess the affected product, and quarantine it if required."
		preventive_action = "Improve temperature monitoring, storage controls, and staff training."
	elif root_cause == "Delivery/transport issue":
		corrective_action = "Investigate the shipment with the carrier and inspect or replace affected products."
		preventive_action = "Strengthen transport controls, packaging checks, and delivery tracking."
	elif root_cause == "Packaging damage":
		corrective_action = "Inspect the affected batch and replace damaged units after quality review."
		preventive_action = "Add packaging-line inspections and handling checks before shipment."
	elif category in ("Quality Issue", "Wrong Product", "Incorrect Product", "Missing Tablets") or severity == "High":
		corrective_action = "Quarantine the affected batch and begin a documented quality investigation."
		preventive_action = "Review manufacturing controls, batch checks, and operator training."
	else:
		corrective_action = "Review the complaint details and resolve the affected customer case."
		preventive_action = "Track complaint trends and improve the relevant process if repeat issues occur."

	return {
		"category": category,
		"severity": severity,
		"priority": priority,
		"summary": summary,
		"root_cause": root_cause,
		"corrective_action": corrective_action,
		"preventive_action": preventive_action,
	}
