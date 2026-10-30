
import sys
import os
from xml.dom import minidom


def generate_vnc_files(xml_file, save_dir):

    print(f"Reading XML file: {xml_file}")

    xml_data = minidom.parse(xml_file)

    os.makedirs(save_dir, exist_ok=True)

    files = xml_data.getElementsByTagName("file")

    print(f"Found {len(files)} connections.")

    for file_node in files:

        name = file_node.getAttribute("name")

        host = ""
        identity = ""
        password = ""

        for section in file_node.getElementsByTagName("section"):

            for param in section.getElementsByTagName("param"):

                param_name = param.getAttribute("name")
                param_value = param.getAttribute("value")

                if param_name == "Host":
                    host = param_value

                elif param_name == "UserName":
                    identity = param_value

                elif param_name == "Password":
                    password = param_value

        if not host:
            print(f"Skipping {name}: No Host found.")
            continue

        content = [
            "ConnMethod=tcp\n",
            f"FriendlyName={name}\n",
            f"Host={host}\n",
            f"Identity={identity}\n",
            f"Password={password}\n"
        ]

        save_path = os.path.join(save_dir, f"{name}.vnc")

        with open(save_path, "w", encoding="utf-8") as save_file:
            save_file.writelines(content)

        print(f"Created: {save_path}")


def main():

    if len(sys.argv) > 3:
        print("Too many arguments.")
        sys.exit(1)

    if len(sys.argv) == 3:
        xml_file = sys.argv[1]
        save_dir = sys.argv[2]

    else:
        xml_file = input("Enter RealVNC's XML file: ").strip()
        save_dir = input("Enter saving directory: ").strip()

    if not os.path.isfile(xml_file):
        print(f"XML file not found: {xml_file}")
        sys.exit(1)

    try:
        generate_vnc_files(xml_file, save_dir)

        print("\nConversion completed!")

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
