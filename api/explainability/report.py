from pathlib import Path
from datetime import datetime

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Image,

    Table,

    TableStyle

)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib import colors

from reportlab.lib.units import inch

from reportlab.lib.enums import TA_CENTER

from reportlab.pdfbase import pdfmetrics


class ExplainabilityReport:

    def __init__(

        self,

        output_directory="reports"

    ):

        self.output_directory = Path(

            output_directory

        )

        self.output_directory.mkdir(

            parents=True,

            exist_ok=True

        )

        self.styles = getSampleStyleSheet()

        self.title_style = self.styles["Heading1"]

        self.title_style.alignment = TA_CENTER

        self.heading_style = self.styles["Heading2"]

        self.normal_style = self.styles["BodyText"]

    # =====================================================
    # DOCUMENT
    # =====================================================

    def create_document(

        self,

        filename="Laptop_Report.pdf"

    ):

        pdf_path = self.output_directory / filename

        document = SimpleDocTemplate(

            str(pdf_path)

        )

        story = []

        return document, story, pdf_path

    # =====================================================
    # TITLE
    # =====================================================

    def add_title(

        self,

        story,

        title="Laptop Explainability Report"

    ):

        story.append(

            Paragraph(

                title,

                self.title_style

            )

        )

        story.append(

            Spacer(

                1,

                0.30 * inch

            )

        )

    # =====================================================
    # TIMESTAMP
    # =====================================================

    def add_timestamp(

        self,

        story

    ):

        current_time = datetime.now().strftime(

            "%d %B %Y %I:%M:%S %p"

        )

        story.append(

            Paragraph(

                f"<b>Generated:</b> {current_time}",

                self.normal_style

            )

        )

        story.append(

            Spacer(

                1,

                0.20 * inch

            )

        )

    # =====================================================
    # SECTION
    # =====================================================

    def add_heading(

        self,

        story,

        heading

    ):

        story.append(

            Paragraph(

                heading,

                self.heading_style

            )

        )

        story.append(

            Spacer(

                1,

                0.15 * inch

            )

        )

    # =====================================================
    # PARAGRAPH
    # =====================================================

    def add_paragraph(

        self,

        story,

        text

    ):

        story.append(

            Paragraph(

                text,

                self.normal_style

            )

        )

        story.append(

            Spacer(

                1,

                0.10 * inch

            )

        )
            # =====================================================
    # TABLE
    # =====================================================

    def add_table(

        self,

        story,

        data,

        column_widths=None

    ):

        table = Table(

            data,

            colWidths=column_widths

        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                ("FONTSIZE",(0,0),(-1,-1),10),

                ("BOTTOMPADDING",(0,0),(-1,0),10),

                ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                ("VALIGN",(0,0),(-1,-1),"MIDDLE")

            ])

        )

        story.append(table)

        story.append(

            Spacer(

                1,

                0.25 * inch

            )

        )

    # =====================================================
    # LAPTOP SPECIFICATIONS
    # =====================================================

    def add_laptop_information(

        self,

        story,

        laptop_data

    ):

        self.add_heading(

            story,

            "Laptop Specifications"

        )

        table = [

            [

                "Feature",

                "Value"

            ]

        ]

        for key, value in laptop_data.items():

            table.append([

                str(key),

                str(value)

            ])

        self.add_table(

            story,

            table,

            column_widths=[2.5*inch,3.5*inch]

        )

    # =====================================================
    # PREDICTION
    # =====================================================

    def add_prediction(

        self,

        story,

        predicted_price,

        predicted_category

    ):

        self.add_heading(

            story,

            "Prediction"

        )

        table = [

            [

                "Output",

                "Prediction"

            ],

            [

                "Predicted Price",

                f"₹ {predicted_price:,.2f}"

            ],

            [

                "Predicted Category",

                predicted_category

            ]

        ]

        self.add_table(

            story,

            table,

            column_widths=[3*inch,3*inch]

        )

    # =====================================================
    # SHAP TABLE
    # =====================================================

    def add_shap_table(

        self,

        story,

        shap_features

    ):

        self.add_heading(

            story,

            "Top SHAP Features"

        )

        table = [

            [

                "Feature",

                "Impact",

                "Direction"

            ]

        ]

        for feature in shap_features:

            table.append([

                feature["feature"],

                f'{feature["impact"]:.5f}',

                feature["direction"]

            ])

        self.add_table(

            story,

            table,

            column_widths=[3*inch,1.3*inch,1.3*inch]

        )

    # =====================================================
    # LIME TABLE
    # =====================================================

    def add_lime_table(

        self,

        story,

        lime_features

    ):

        self.add_heading(

            story,

            "Top LIME Features"

        )

        table = [

            [

                "Feature",

                "Impact",

                "Direction"

            ]

        ]

        for feature in lime_features:

            table.append([

                feature["feature"],

                f'{feature["impact"]:.5f}',

                feature["direction"]

            ])

        self.add_table(

            story,

            table,

            column_widths=[3*inch,1.3*inch,1.3*inch]

        )
            # =====================================================
    # IMAGE
    # =====================================================

    def add_image(

        self,

        story,

        image_path,

        width=6 * inch,

        height=4 * inch

    ):

        image_path = Path(image_path)

        if not image_path.exists():

            return

        story.append(

            Image(

                str(image_path),

                width=width,

                height=height

            )

        )

        story.append(

            Spacer(

                1,

                0.25 * inch

            )

        )

    # =====================================================
    # SHAP PLOTS
    # =====================================================

    def add_shap_plots(

        self,

        story,

        shap_paths

    ):

        self.add_heading(

            story,

            "SHAP Visualizations"

        )

        plot_names = {

            "waterfall": "Waterfall Plot",

            "bar": "Feature Importance",

            "beeswarm": "Beeswarm Plot",

            "decision": "Decision Plot"

        }

        for key, title in plot_names.items():

            if key in shap_paths:

                story.append(

                    Paragraph(

                        f"<b>{title}</b>",

                        self.normal_style

                    )

                )

                self.add_image(

                    story,

                    shap_paths[key]

                )

    # =====================================================
    # BUILD PDF
    # =====================================================

    def build(

        self,

        document,

        story

    ):

        document.build(

            story

        )

    # =====================================================
    # COMPLETE REPORT
    # =====================================================

    def generate_report(

        self,

        laptop_information,

        predicted_price,

        predicted_category,

        shap_result,

        lime_result,

        filename="Laptop_Report.pdf"

    ):

        document, story, pdf_path = self.create_document(

            filename

        )

        self.add_title(

            story

        )

        self.add_timestamp(

            story

        )

        self.add_laptop_information(

            story,

            laptop_information

        )

        self.add_prediction(

            story,

            predicted_price,

            predicted_category

        )

        self.add_shap_table(

            story,

            shap_result["top_features"]

        )

        self.add_lime_table(

            story,

            lime_result["top_features"]

        )

        if "plots" in shap_result:

            self.add_shap_plots(

                story,

                shap_result["plots"]

            )

        self.build(

            document,

            story

        )

        return str(pdf_path)

    # =====================================================
    # QUICK REPORT
    # =====================================================

    def __call__(

        self,

        laptop_information,

        predicted_price,

        predicted_category,

        shap_result,

        lime_result,

        filename="Laptop_Report.pdf"

    ):

        return self.generate_report(

            laptop_information,

            predicted_price,

            predicted_category,

            shap_result,

            lime_result,

            filename

        )