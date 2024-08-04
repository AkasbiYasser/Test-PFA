# Text-messaging-generation-software-via-SMPP

Enviar SMS is a robust text messaging generation software utilizing the SMPP protocol. The project is designed to facilitate the sending of SMS messages from one server to another via multiple providers, with acknowledgment of message receipt.

Introduction This software allows users to send SMS messages from one server (Server 1) to another (Server 2) through multiple suppliers. Upon delivery, a "DLR" signal is sent back to the originating server to confirm receipt.

Features Input Module: Allows uploading and displaying CSV files containing SMS destination data. Suppliers Module: Manages suppliers with configurable parameters. Generator Module: Generates and schedules SMS messages based on templates. Reporting Module: Generates detailed reports on SMS activity. Modules Server 1 This server handles sending SMS messages. It includes the following modules:

Input Module:

Upload CSV files. Display data such as SID, Destination, and Message. Suppliers Module:

Manage suppliers with fields for Name, IP, Port, User, and Password. Generation Module:

Create, modify, and delete SMS templates. Schedule SMS sending tasks. Enable/Disable suppliers. Repeat SMS sending if all messages are sent before the scheduled time ends. Reporting Module:

Generate reports by date range, supplier, and message status. Visualize message statistics and comparisons. Server 2 This server handles receiving SMS messages. It includes the following modules:

Client Module:

Create, modify, and delete clients. Manage client fields: Name, IP, Port, User, and Password. Reporting Module:

Generate reports on received messages. Visualize statistics of messages received by customers. Usage Setup and Configure Servers:

Configure Server 1 to send SMS messages through selected suppliers. Set up Server 2 to receive messages and send DLR signals. Upload CSV Files:

Use the Input Module on Server 1 to upload destination data. Manage Suppliers and Clients:

Use the Suppliers and Client Modules to configure suppliers and clients. Generate and Schedule SMS Messages:

Create templates and schedule sending tasks in the Generation Module. Monitor and Report:

Use the Reporting Module to generate and review detailed reports. Requirements SMPP protocol support. Servers configured to handle SMS sending and receiving. Database to manage suppliers, clients, and reports.
