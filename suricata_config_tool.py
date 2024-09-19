import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog, QMessageBox

class SuricataRulesManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Suricata Rules Manager")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Suricata Rules Configuration Tool", self)
        layout.addWidget(self.label)

        # List widget to display rules
        self.rules_list = QListWidget(self)
        layout.addWidget(self.rules_list)

        # Buttons
        self.load_button = QPushButton("Load Rules File", self)
        self.load_button.clicked.connect(self.load_rules_file)
        layout.addWidget(self.load_button)

        self.enable_button = QPushButton("Enable Selected Rule", self)
        self.enable_button.clicked.connect(self.enable_rule)
        layout.addWidget(self.enable_button)

        self.disable_button = QPushButton("Disable Selected Rule", self)
        self.disable_button.clicked.connect(self.disable_rule)
        layout.addWidget(self.disable_button)

        self.save_button = QPushButton("Save Changes", self)
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # Initialize rules file and list of rules
        self.rules_file_path = None
        self.rules_data = []

    def load_rules_file(self):
        # Open file dialog to select a rules file
        self.rules_file_path, _ = QFileDialog.getOpenFileName(self, "Open Suricata Rules File", "", "Rules Files (*.rules *.yaml)")
        
        if self.rules_file_path:
            self.rules_list.clear()
            try:
                # Read the file and load rules into list widget
                with open(self.rules_file_path, 'r') as f:
                    self.rules_data = f.readlines()

                for line in self.rules_data:
                    self.rules_list.addItem(line.strip())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

    def enable_rule(self):
        # Enable the selected rule (remove leading comment)
        selected_item = self.rules_list.currentItem()
        if selected_item:
            rule = selected_item.text()
            if rule.startswith('#'):
                new_rule = rule[1:].strip()
                selected_item.setText(new_rule)
                self.update_rule_in_file(rule, new_rule)
            else:
                QMessageBox.information(self, "Info", "Rule is already enabled.")
        else:
            QMessageBox.warning(self, "Warning", "No rule selected.")

    def disable_rule(self):
        # Disable the selected rule (add leading comment)
        selected_item = self.rules_list.currentItem()
        if selected_item:
            rule = selected_item.text()
            if not rule.startswith('#'):
                new_rule = '# ' + rule
                selected_item.setText(new_rule)
                self.update_rule_in_file(rule, new_rule)
            else:
                QMessageBox.information(self, "Info", "Rule is already disabled.")
        else:
            QMessageBox.warning(self, "Warning", "No rule selected.")

    def update_rule_in_file(self, old_rule, new_rule):
        # Update the rule in the data
        for i in range(len(self.rules_data)):
            if self.rules_data[i].strip() == old_rule:
                self.rules_data[i] = new_rule + '\n'
                break

    def save_changes(self):
        # Save the changes to the rules file
        if self.rules_file_path and self.rules_data:
            try:
                with open(self.rules_file_path, 'w') as f:
                    f.writelines(self.rules_data)
                QMessageBox.information(self, "Success", "Rules file saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "No file loaded or no changes made.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SuricataRulesManager()
    window.show()
    sys.exit(app.exec_())
