from PyQt4.QtGui import QCheckBox, QFormLayout, QLabel, QLineEdit, QVBoxLayout

from neuropype.nodes.network import LSLInput

from .quickstartwizarddialog import QuickstartWizardDialog


class SpectralBandpowerQuickstartWizardDialog(QuickstartWizardDialog):
    def get_custom_layout(self):
        custom_layout = QVBoxLayout()
        custom_layout.setContentsMargins(12, 12, 12, 12)

        template = '<h4>{0}</h4>'

        ######## Step 1

        step_1 = QLabel(template.format(self.tr("What data stream do you want to read from? (e.g., name='Cognionics'):")))
        step_1.setContentsMargins(0, 5, 0, 0)

        # Query.
        default_query = LSLInput.port('query').default
        query = QLineEdit(str(default_query), self)

        custom_layout.addWidget(step_1)
        custom_layout.addWidget(query)

        ######## Step 4

        step_4 = QLabel(template.format(self.tr('Next you can define the EEG frequency range of interest:')))
        step_4.setContentsMargins(0, 15, 0, 0)

        # Low transition start.
        low_transition_start = QLineEdit(str(6), self)

        # Low transition end.
        low_transition_end = QLineEdit(str(8), self)

        # High transition start.
        high_transition_start = QLineEdit(str(12), self)

        # High transition end.
        high_transition_end = QLineEdit(str(15), self)

        # Form layout.
        bandpass_form = QFormLayout()
        bandpass_form.addRow(self.tr('Pass-band up-ramp start frequency'), low_transition_start)
        bandpass_form.addRow(self.tr('Pass-band up-ramp end frequency'), low_transition_end)
        bandpass_form.addRow(self.tr('Pass-band down-ramp start frequency'), high_transition_start)
        bandpass_form.addRow(self.tr('Pass-band down-ramp end frequency'), high_transition_end)

        custom_layout.addWidget(step_4)
        custom_layout.addLayout(bandpass_form)

        ######## Step 5

        step_5 = QLabel(template.format(self.tr("Please choose the names of the output streams:")))
        step_5.setContentsMargins(0, 15, 0, 0)

        # Raw-data outlet.
        raw_outlet = QLineEdit('pyBCILAB:Raw', self)

        # Spectrum outlet.
        spectrum_outlet = QLineEdit('pyBCILAB:Spectrum', self)

        # Alpha outlet.
        alpha_outlet = QLineEdit('pyBCILAB:Alpha', self)

        # Form layout.
        outlet_form = QFormLayout()
        outlet_form.addRow(self.tr('Raw Data'), raw_outlet)
        outlet_form.addRow(self.tr('Power Spectrum'), spectrum_outlet)
        outlet_form.addRow(self.tr('Retained Band'), alpha_outlet)

        custom_layout.addWidget(step_5)
        custom_layout.addLayout(outlet_form)

        ######## Attributes
        self._query = query
        self._low_transition_start = low_transition_start
        self._low_transition_end = low_transition_end
        self._high_transition_start = high_transition_start
        self._high_transition_end = high_transition_end
        self._raw_outlet = raw_outlet
        self._spectrum_outlet = spectrum_outlet
        self._alpha_outlet = alpha_outlet

        return custom_layout

    def get_patch(self):
        return {
            'LSL Input': {
                'query': self._query.text()
            },
            'IIR Bandpass': {
                'frequencies': '({0}, {1}, {2}, {3})'.format(self._low_transition_start.text(),
                                                             self._low_transition_end.text(),
                                                             self._high_transition_start.text(),
                                                             self._high_transition_end.text()),
            },
            'Raw Outlet': {
                'stream_name': self._raw_outlet.text()
            },
            'Spectrum Outlet': {
                'stream_name': self._spectrum_outlet.text()
            },
            'Alpha Outlet': {
                'stream_name': self._alpha_outlet.text()
            }
        }
