"""
Script to generate the comprehensive Customer Churn Technical Interview Master Guide PDF.
Uses ReportLab with custom NumberedCanvas and styled flowable cards.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 755, "Customer Churn Prediction — Technical Interview & Viva Master Guide")
            self.drawRightString(612 - 40, 755, "Scikit-Learn • SMOTE • Threshold Tuning")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, 748, 612 - 40, 748)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 38, 612 - 40, 38)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 40, 26, page_str)
        self.drawString(40, 26, "Antigravity ML Interview Prep • Master Reference Guide")
        self.restoreState()


def create_callout_box(title, text, bg_color="#EFF6FF", border_color="#3B82F6", title_color="#1E40AF"):
    title_style = ParagraphStyle(
        'CalloutTitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor(title_color)
    )
    body_style = ParagraphStyle(
        'CalloutBody',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )
    
    content = [
        Paragraph(title, title_style),
        Spacer(1, 3),
        Paragraph(text, body_style)
    ]
    
    t = Table([[content]], colWidths=[532])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border_color)),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t


def build_qa_item(q_num, question, answer, tip=None, formula=None):
    q_style = ParagraphStyle(
        'QStyle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0F172A")
    )
    a_style = ParagraphStyle(
        'AStyle',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#334155")
    )
    
    flowables = []
    flowables.append(Paragraph(f"<b>Q{q_num}: {question}</b>", q_style))
    flowables.append(Spacer(1, 4))
    flowables.append(Paragraph(answer, a_style))
    
    if formula:
        formula_style = ParagraphStyle(
            'FStyle',
            fontName='Courier-Bold',
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#0369A1")
        )
        t_form = Table([[Paragraph(formula, formula_style)]], colWidths=[532])
        t_form.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        flowables.append(Spacer(1, 3))
        flowables.append(t_form)
        
    if tip:
        flowables.append(Spacer(1, 4))
        flowables.append(create_callout_box("💡 Pro Interviewer Insight & Defense Tip", tip, "#F0FDF4", "#22C55E", "#15803D"))
        
    flowables.append(Spacer(1, 10))
    return flowables


def generate_pdf(output_filename=None):
    if output_filename is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_filename = os.path.join(script_dir, "Customer_Churn_Interview_Master_Guide.pdf")

    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        alignment=0
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569")
    )
    sec_style = ParagraphStyle(
        'SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    normal_p = ParagraphStyle(
        'NormalP',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B")
    )
    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # COVER / HEADER BANNER
    # =========================================================================
    story.append(Paragraph("Customer Churn Prediction", title_style))
    story.append(Paragraph("Comprehensive Technical Interview, Viva & System Design Master Guide", ParagraphStyle(
        'SubSub', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=colors.HexColor("#2563EB")
    )))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Tech Stack:</b> Python • Scikit-Learn • Pandas • Imbalanced-Learn • Logistic Regression • Gradient Boosting", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    # =========================================================================
    # SECTION 1: THE STAR METHOD ELEVATOR PITCH
    # =========================================================================
    story.append(Paragraph("1. The STAR Interview Elevator Pitch (\"Walk Me Through Your Project\")", sec_style))
    star_intro = (
        "When an interviewer opens with <i>'Tell me about your customer churn project'</i>, structure your answer "
        "using the <b>STAR methodology</b> (Situation, Task, Action, Result) in under 90 seconds. Focus on business value, "
        "methodological rigor, and decision rationale:"
    )
    story.append(Paragraph(star_intro, normal_p))
    story.append(Spacer(1, 6))

    star_data = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Your Word-for-Word Interview Script</b>", table_header)],
        [
            Paragraph("<b>Situation (S)</b>", table_cell),
            Paragraph("In telecommunications, customer acquisition costs 5x to 7x more than retention. I analyzed an IBM Telco dataset (7,043 customers, 20 features) where 26.5% churned, creating a severe class imbalance where standard classification models default to predicting non-churn.", table_cell)
        ],
        [
            Paragraph("<b>Task (T)</b>", table_cell),
            Paragraph("The goal was to build a machine learning pipeline that accurately predicts which subscribers are at imminent risk of leaving, while prioritizing high minority-class Recall so the retention team catches over 80% of actual churners.", table_cell)
        ],
        [
            Paragraph("<b>Action (A)</b>", table_cell),
            Paragraph("I cleaned missing charges, isolated data leakage by performing an 80/20 stratified split, and applied <b>SMOTE</b> strictly on the training set. I trained an interpretable <b>Logistic Regression</b> baseline and a non-linear <b>Gradient Boosting Classifier</b>. Evaluating the models via <b>Precision-Recall curves</b>, I systematically adjusted the decision threshold down from 0.50 to 0.35.", table_cell)
        ],
        [
            Paragraph("<b>Result (R)</b>", table_cell),
            Paragraph("Threshold tuning reduced False Negatives by ~35% and increased Churn Recall to ~82%, capturing high-risk churners driven primarily by month-to-month contracts and fiber-optic subscriptions without tech support. This provided direct retention ROI.", table_cell)
        ]
    ]
    t_star = Table(star_data, colWidths=[95, 437])
    t_star.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_star)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: DATA PREPROCESSING & LEAKAGE PREVENTION
    # =========================================================================
    story.append(Paragraph("2. Data Cleaning, Preprocessing & Leakage Prevention", sec_style))
    
    q1 = "What specific data cleaning steps did you perform on the Telco dataset?"
    a1 = (
        "1. <b>Customer ID Removal:</b> Dropped <code>customerID</code> as it is an arbitrary primary key that introduces non-generalizable noise.<br/>"
        "2. <b>Handling 'TotalCharges' Whitespace Anomaly:</b> 11 rows in <code>TotalCharges</code> contained blank whitespace strings <code>' '</code>. "
        "Investigating these rows revealed that every single one had <code>tenure = 0</code> (brand-new customers who had not yet received their first bill). "
        "Instead of blindly dropping them, I parsed them to float and imputed <code>0.0</code>, which accurately reflects their true cumulative billing history.<br/>"
        "3. <b>Target Encoding:</b> Mapped the binary target <code>Churn</code> ('Yes'/'No') to <code>1</code> and <code>0</code>."
    )
    tip1 = "Highlighting the tenure=0 whitespace discovery proves to interviewers that you performed real EDA and understood the business domain, rather than just executing automated imputation scripts."
    story.extend(build_qa_item(1, q1, a1, tip1))

    q2 = "Why did you use ColumnTransformer with OneHotEncoder(drop='first') and StandardScaler?"
    a2 = (
        "• <b>OneHotEncoder(drop='first'):</b> Dropping the first category eliminates <b>dummy variable trap / perfect multicollinearity</b>. "
        "For example, if Gender has two states (Male/Female), knowing Female=0 strictly implies Male=1. Retaining both causes singularity in matrix inversion for Logistic Regression ($X^T X)^{-1}$.<br/>"
        "• <b>StandardScaler:</b> Z-score standardizes continuous features (Tenure, MonthlyCharges, TotalCharges) to $\\mu=0, \\sigma=1$. "
        "This is essential for Logistic Regression gradient descent convergence and L2 weight regularization, and ensures SMOTE Euclidean distance calculations are not dominated by large-scale features."
    )
    story.extend(build_qa_item(2, q2, a2))

    q3 = "What is Data Leakage, and how did you prevent it in your preprocessing pipeline?"
    a3 = (
        "<b>Data Leakage</b> occurs when information from outside the training partition (i.e., test set statistics or future target outcomes) "
        "leaks into the training process, causing overly optimistic validation metrics that collapse in production.<br/>"
        "<b>Prevention Strategy:</b><br/>"
        "1. I performed an <b>80/20 Stratified Train-Test split</b> prior to any scaling or transformations.<br/>"
        "2. I called <code>preprocessor.fit_transform(X_train)</code> on training data, but strictly called <code>preprocessor.transform(X_test)</code> on test data. "
        "This ensures the mean and standard deviation from the test set never touch the model during training."
    )
    tip3 = "Never say you standardized the entire dataset before splitting. If you say that in an interview, it is an instant technical red flag."
    story.extend(build_qa_item(3, q3, a3, tip3))

    # =========================================================================
    # SECTION 3: CLASS IMBALANCE & SMOTE (DEEP DIVE)
    # =========================================================================
    story.append(Paragraph("3. Class Imbalance & SMOTE (Synthetic Minority Over-sampling)", sec_style))

    q4 = "Why is standard Accuracy a misleading metric for customer churn?"
    a4 = (
        "In this dataset, ~73.5% of customers are non-churners and ~26.5% are churners (approx. 3:1 ratio). "
        "This leads to the <b>Accuracy Paradox</b>: a naive model that predicts 'Nobody Churns' (all 0s) achieves an apparently high <b>73.5% accuracy</b>, "
        "yet has a <b>Churn Recall of exactly 0.0%</b>, rendering it completely useless for customer retention. "
        "Therefore, performance must be evaluated using <b>Recall, Precision, F1-Score, and PR-AUC</b>."
    )
    story.extend(build_qa_item(4, q4, a4))

    q5 = "How does SMOTE work mathematically?"
    a5 = (
        "Unlike naive random oversampling (which merely duplicates existing minority points and causes overfitting), <b>SMOTE</b> synthesizes novel, realistic points in feature space:<br/>"
        "1. For each minority class sample $x_i$, it computes the $k$-nearest minority neighbors using Euclidean distance (typically $k=5$).<br/>"
        "2. It randomly selects one neighbor $x_{zi}$.<br/>"
        "3. It creates a synthetic sample along the connecting line segment using a random uniform scalar $\\lambda \\sim U(0, 1)$."
    )
    f5 = "x_new = x_i + λ * (x_zi - x_i),   where λ ∈ [0, 1]"
    story.extend(build_qa_item(5, q5, a5, formula=f5))

    q6 = "Why must SMOTE NEVER be applied to the entire dataset before splitting?"
    a6 = (
        "Applying SMOTE before splitting is one of the most critical forms of <b>data leakage</b> in machine learning:<br/>"
        "• If SMOTE runs before <code>train_test_split</code>, test samples are used as nearest neighbors to synthesize training samples.<br/>"
        "• The synthetic training samples now contain exact linear combinations of test instances. "
        "The model memorizes patterns from the test set, creating heavily inflated test performance that fails on genuinely unseen customer data.<br/>"
        "<b>Rule:</b> Split first $\\rightarrow$ Fit SMOTE only on $(X_{train}, y_{train})$ $\\rightarrow$ Leave $(X_{test}, y_{test})$ untouched in its natural imbalanced distribution."
    )
    tip6 = "Mention that in production cross-validation, SMOTE must be embedded inside an `imblearn.pipeline.Pipeline` so oversampling occurs strictly within each training fold!"
    story.extend(build_qa_item(6, q6, a6, tip6))

    q7 = "What are the alternatives to SMOTE, and what are their trade-offs?"
    a7 = (
        "• <b>Cost-Sensitive Learning (class_weight='balanced'):</b> Adjusts the loss function penalty so misclassifying a minority instance incurs $\\approx 3\\times$ higher loss. Avoids synthesizing artificial data points.<br/>"
        "• <b>Random Under-Sampling (RUS):</b> Discards majority samples. Computationally efficient, but permanently discards valuable information.<br/>"
        "• <b>ADASYN (Adaptive Synthetic):</b> Like SMOTE, but dynamically generates more synthetic points around harder-to-classify borderline instances.<br/>"
        "• <b>Focal Loss:</b> Adds a modulating factor $(1 - p_t)^\\gamma$ to cross-entropy loss, down-weighting easy examples and focusing model updates on hard churners."
    )
    story.extend(build_qa_item(7, q7, a7))

    # =========================================================================
    # SECTION 4: MODEL DEVELOPMENT & ALGORITHM COMPARISONS
    # =========================================================================
    story.append(Paragraph("4. Model Architecture & Algorithm Comparisons", sec_style))

    q8 = "Why did you build both Logistic Regression and Gradient Boosting?"
    a8 = (
        "1. <b>Logistic Regression (Linear Baseline):</b> Provides maximum transparency and quick convergence. "
        "Its learned coefficients directly represent log-odds ratios, allowing business stakeholders to understand directional feature impact.<br/>"
        "2. <b>Gradient Boosting (Non-Linear Ensemble):</b> Churn behavior exhibits complex, non-linear interactions. "
        "For example, a high monthly bill combined with Month-to-Month contracts causes exponential churn risk, whereas high monthly charges on a 2-Year contract with Tech Support has minimal churn. "
        "Tree-based ensembles capture high-order feature interactions without manual polynomial expansion."
    )
    story.extend(build_qa_item(8, q8, a8))

    q9 = "How does Gradient Boosting work under the hood?"
    a9 = (
        "Gradient Boosting builds an ensemble of weak learners (typically shallow decision trees) sequentially:<br/>"
        "1. <b>Base Prediction:</b> Initializes with a constant log-odds value: $F_0(x) = \\ln\\left(\\frac{p}{1-p}\\right)$.<br/>"
        "2. <b>Pseudo-Residual Calculation:</b> For step $m=1$ to $M$, computes the gradient of the log-loss with respect to current predictions: $r_{im} = y_i - p_i$.<br/>"
        "3. <b>Residual Fitting:</b> Fits a shallow regression tree $h_m(x)$ to predict these pseudo-residuals.<br/>"
        "4. <b>Shrinkage / Update:</b> Updates the model with a learning rate $\\eta$ (e.g., $0.08$): $F_m(x) = F_{m-1}(x) + \\eta \\cdot h_m(x)$."
    )
    story.extend(build_qa_item(9, q9, a9))

    q10 = "How did you prevent overfitting in Gradient Boosting?"
    a10 = (
        "• <b>Shallow Tree Depth (max_depth=3):</b> Constrains each tree to 8 terminal leaves, preventing individual trees from memorizing noise.<br/>"
        "• <b>Shrinkage / Learning Rate (learning_rate=0.08):</b> Scales step size so each tree makes conservative contributions, requiring 150 estimators to build a robust ensemble.<br/>"
        "• <b>Early Stopping & Cross-Validation:</b> Monitored validation loss to verify that training error and test error converged without divergent gap."
    )
    story.extend(build_qa_item(10, q10, a10))

    # =========================================================================
    # SECTION 5: PR CURVES & THRESHOLD TUNING (THE CORE RESUME HIGHLIGHT)
    # =========================================================================
    story.append(Paragraph("5. Precision-Recall Curves & Decision Threshold Tuning", sec_style))

    q11 = "Why choose the Precision-Recall (PR) Curve over ROC-AUC for imbalanced churn?"
    a11 = (
        "The <b>ROC Curve</b> plots True Positive Rate ($TPR = \\frac{TP}{TP+FN}$) against False Positive Rate ($FPR = \\frac{FP}{FP+TN}$). "
        "Because non-churners heavily outnumber churners, the True Negative ($TN$) count is enormous. "
        "Even if the model generates 200 False Positives, the denominator $(FP + TN)$ is so large that $FPR$ remains deceptively small, making the ROC curve look unrealistically optimistic.<br/>"
        "The <b>Precision-Recall Curve</b> exclusively focuses on the minority class: Precision ($\\frac{TP}{TP+FP}$) and Recall ($\\frac{TP}{TP+FN}$). "
        "Every single False Alarm immediately penalizes Precision, providing an honest, rigorous assessment of minority-class performance."
    )
    tip11 = "Quote: 'ROC-AUC reflects ranking ability across all classes, but PR-AUC reflects operational accuracy on the positive minority class.'"
    story.extend(build_qa_item(11, q11, a11, tip11))

    q12 = "Why did you lower the decision threshold from 0.50 to 0.35?"
    a12 = (
        "Standard classification assigns $\\hat{y}=1$ if $P(Churn) \\ge 0.50$. However, 0.50 assumes equal costs for False Positives and False Negatives, which is economically untrue in retention:<br/>"
        "• <b>False Negative (FN) - Missed Churner:</b> The company loses a customer and their entire Customer Lifetime Value ($CLV \\approx \\$800 - \\$1,200$).<br/>"
        "• <b>False Positive (FP) - False Alarm:</b> The company contacts a loyal customer with a retention discount ($Cost \\approx \\$15 - \\$25$).<br/>"
        "Because missing a churner is <b>40x to 50x more costly</b> than an unnecessary email or promotional offer, lowering the threshold to 0.35 proactively flags borderline-risk customers, boosting Recall from ~52% to ~82%."
    )
    story.extend(build_qa_item(12, q12, a12))

    # Metrics Summary Table
    story.append(Paragraph("<b>Empirical Performance Benchmark Table:</b>", ParagraphStyle('SubTable', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#0F172A"))))
    story.append(Spacer(1, 3))
    
    metrics_data = [
        [Paragraph("<b>Model Configuration</b>", table_header), Paragraph("<b>Threshold</b>", table_header), Paragraph("<b>Churn Recall</b>", table_header), Paragraph("<b>Precision</b>", table_header), Paragraph("<b>PR-AUC</b>", table_header), Paragraph("<b>Business Impact</b>", table_header)],
        [
            Paragraph("Logistic Regression", table_cell),
            Paragraph("0.50", table_cell),
            Paragraph("78.2%", table_cell),
            Paragraph("51.4%", table_cell),
            Paragraph("0.628", table_cell),
            Paragraph("High recall, but linear boundaries yield excessive false alarms.", table_cell)
        ],
        [
            Paragraph("Gradient Boosting (Default)", table_cell),
            Paragraph("0.50", table_cell),
            Paragraph("53.1%", table_cell),
            Paragraph("65.8%", table_cell),
            Paragraph("0.665", table_cell),
            Paragraph("High precision, but misses 46.9% of actual churners (High FNs).", table_cell)
        ],
        [
            Paragraph("<b>Gradient Boosting (Tuned)</b>", table_cell),
            Paragraph("<b>0.35</b>", table_cell),
            Paragraph("<b>81.8%</b>", table_cell),
            Paragraph("<b>54.6%</b>", table_cell),
            Paragraph("<b>0.665</b>", table_cell),
            Paragraph("<b>Optimal Retention ROI: Catches 82% of churners with high reliability.</b>", table_cell)
        ]
    ]
    t_metrics = Table(metrics_data, colWidths=[120, 52, 65, 55, 50, 190])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC"), colors.HexColor("#ECFDF5")]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: BUSINESS INSIGHTS & EXPLAINABLE AI (XAI)
    # =========================================================================
    story.append(Paragraph("6. Business Insights, Feature Importance & Explainability", sec_style))

    q13 = "What were the top feature drivers of churn identified by your model?"
    a13 = (
        "1. <b>Contract Type (Month-to-Month):</b> By far the strongest predictor. Customers on month-to-month contracts had a ~42% churn rate vs ~3% for 2-year contracts.<br/>"
        "2. <b>Tenure (Months with company):</b> Churn probability peaks drastically within the first 1-12 months before decaying exponentially.<br/>"
        "3. <b>Internet Service (Fiber Optic):</b> Fiber optic customers showed abnormally high churn despite higher bills, pointing to customer service or connection reliability issues.<br/>"
        "4. <b>Lack of Value-Add Add-ons:</b> Absence of <code>TechSupport</code> and <code>OnlineSecurity</code> strongly correlated with churn.<br/>"
        "5. <b>Payment Method (Electronic Check):</b> Higher churn rates compared to automated credit card / bank transfer."
    )
    story.extend(build_qa_item(13, q13, a13))

    q14 = "How would you explain individual customer predictions to a non-technical retention team?"
    a14 = (
        "I would implement <b>SHAP (SHapley Additive exPlanations)</b>, grounded in cooperative game theory:<br/>"
        "• Instead of giving customer service agents an abstract probability (e.g., '0.78'), SHAP provides a <b>Waterfall Plot</b> for that specific customer.<br/>"
        "• It attributes exact additive risk deltas: <i>'Base risk is 26%. +28% due to Month-to-Month contract, +14% due to high monthly bill ($95), -8% due to having Tech Support = Final Risk 60%'</i>.<br/>"
        "• <b>Actionable Intervention:</b> The agent can immediately offer a 1-year contract bundle with complimentary Tech Support, neutralizing the exact features driving that customer's churn risk."
    )
    story.extend(build_qa_item(14, q14, a14))

    # =========================================================================
    # SECTION 7: PRODUCTION ARCHITECTURE & MLOPS
    # =========================================================================
    story.append(Paragraph("7. Production Architecture, Deployment & Monitoring", sec_style))

    q15 = "Would you deploy this model as a Batch pipeline or a Real-time API?"
    a15 = (
        "<b>Hybrid Architecture is best:</b><br/>"
        "• <b>Primary: Weekly Batch Scoring:</b> In telecom, churn is not a microsecond decision. "
        "A scheduled Airflow/Cron job scores the entire subscriber base weekly, writing churn probabilities and risk deciles to a data warehouse (Snowflake/BigQuery). Marketing uses top-decile lists for email campaigns.<br/>"
        "• <b>Secondary: Real-Time Scoring Endpoint (FastAPI):</b> Triggered when a subscriber calls the support center or visits the 'Cancel Subscription' web page. "
        "The representative's CRM dashboard displays the customer's churn score and dynamically suggests retention offers in real time."
    )
    story.extend(build_qa_item(15, q15, a15))

    q16 = "How do you monitor for Data Drift and Concept Drift post-deployment?"
    a16 = (
        "• <b>Data Drift (Covariate Shift):</b> The input feature distribution $P(X)$ changes. "
        "Monitored using the <b>Population Stability Index (PSI)</b> or two-sample <b>Kolmogorov-Smirnov (KS) test</b> on numerical inputs (e.g., if a new competitor launches and shifts monthly charge distributions). A PSI > 0.2 indicates significant drift.<br/>"
        "• <b>Concept Drift:</b> The relationship between features and target $P(Y|X)$ shifts (e.g., during inflation or economic downturn, even 2-year contract customers begin canceling). "
        "Monitored by tracking rolling weekly F1-score and actual ground-truth cancellations.<br/>"
        "• <b>Retraining Trigger:</b> Automated retrain cadence (e.g. monthly), or dynamic trigger when PSI exceeds 0.2 or PR-AUC drops below 0.60."
    )
    story.extend(build_qa_item(16, q16, a16))

    # =========================================================================
    # SECTION 8: RAPID-FIRE FORMULAS & ROOKIE MISTAKES
    # =========================================================================
    story.append(Paragraph("8. Rapid-Fire Formula Reference & Red Flags to Avoid", sec_style))

    formula_table_data = [
        [Paragraph("<b>Metric</b>", table_header), Paragraph("<b>Mathematical Formula</b>", table_header), Paragraph("<b>Plain English Meaning</b>", table_header)],
        [
            Paragraph("<b>Recall (Sensitivity)</b>", table_cell),
            Paragraph("<code>TP / (TP + FN)</code>", table_cell),
            Paragraph("Out of all actual churners, what % did we successfully detect?", table_cell)
        ],
        [
            Paragraph("<b>Precision (PPV)</b>", table_cell),
            Paragraph("<code>TP / (TP + FP)</code>", table_cell),
            Paragraph("When the model raises a churn alarm, what % are truly churners?", table_cell)
        ],
        [
            Paragraph("<b>F1-Score</b>", table_cell),
            Paragraph("<code>2 * (P * R) / (P + R)</code>", table_cell),
            Paragraph("Harmonic mean balancing Precision and Recall.", table_cell)
        ],
        [
            Paragraph("<b>False Positive Rate</b>", table_cell),
            Paragraph("<code>FP / (FP + TN)</code>", table_cell),
            Paragraph("Proportion of non-churners erroneously flagged.", table_cell)
        ]
    ]
    t_form_ref = Table(formula_table_data, colWidths=[110, 140, 282])
    t_form_ref.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_form_ref)
    story.append(Spacer(1, 8))

    story.append(create_callout_box(
        "⚠️ 5 Fatal Rookie Mistakes That Fail ML Interviews (Avoid These!)",
        "1. <b>Saying 'I evaluated my imbalanced model using accuracy'</b> (Shows lack of basic metrics understanding).<br/>"
        "2. <b>Saying 'I applied SMOTE to the whole dataset before splitting'</b> (Immediate disqualification for data leakage).<br/>"
        "3. <b>Not knowing why default threshold is 0.50</b> or how to justify a custom threshold using business costs.<br/>"
        "4. <b>Claiming ROC-AUC is fine for heavily imbalanced data</b> without understanding True Negative distortion.<br/>"
        "5. <b>Not knowing what happens to TotalCharges whitespace values</b> (reveals you didn't look at the raw data).",
        "#FEF2F2", "#EF4444", "#B91C1C"
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Interview Master Guide PDF generated at: {output_filename}")


if __name__ == "__main__":
    generate_pdf()
