import Evtx.Evtx as evtx
from lxml import etree

def parse_events(evtx_path):
    events = []
    with evtx.Evtx(evtx_path) as log:
        for record in log.records():
            try:
                xml = record.xml()
                root = etree.fromstring(xml.encode('utf-8'))

                # SYSTEM FIELDS
                system = root.find("{http://schemas.microsoft.com/win/2004/08/events/event}System")
                event_id_elem = system.find("{http://schemas.microsoft.com/win/2004/08/events/event}EventID")
                time_created_elem = system.find("{http://schemas.microsoft.com/win/2004/08/events/event}TimeCreated")
                provider_elem = system.find("{http://schemas.microsoft.com/win/2004/08/events/event}Provider")
                security_elem = system.find("{http://schemas.microsoft.com/win/2004/08/events/event}Security")

                event_id = int(event_id_elem.text) if event_id_elem is not None else 0
                timestamp = time_created_elem.get("SystemTime") if time_created_elem is not None else "Unknown"
                provider = provider_elem.get("Name") if provider_elem is not None else "Unknown"
                user = security_elem.get("UserID") if security_elem is not None else "Unknown"

                # EVENTDATA (MESSAGE)
                event_data_elem = root.find("{http://schemas.microsoft.com/win/2004/08/events/event}EventData")
                if event_data_elem is not None:
                    message_parts = []
                    for data in event_data_elem.findall("{http://schemas.microsoft.com/win/2004/08/events/event}Data"):
                        if data.text:
                            message_parts.append(data.text.strip())
                    message = " | ".join(message_parts) if message_parts else "No message"
                else:
                    message = "No message"

                events.append({
                    "EventID": event_id,
                    "Timestamp": timestamp,
                    "Provider": provider,
                    "User": user if user else "Unknown",
                    "Message": message
                })

            except Exception as e:
                print(f"Failed to parse a record: {e}")

    return events
