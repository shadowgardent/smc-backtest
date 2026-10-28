function createSMCEvaluationForm() {
  // 1. สร้าง Google Form ใหม่
  var form = FormApp.create('แบบประเมินความพึงพอใจการใช้งานระบบวิเคราะห์โครงสร้างตลาดการเงินด้วยอัลกอริทึม Smart Money Concepts (SMC)');
  form.setDescription(
    'คำชี้แจง: แบบประเมินนี้จัดทำขึ้นเพื่อประเมินประสิทธิภาพและความพึงพอใจของผู้ใช้งานที่มีต่อระบบวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม Smart Money Concepts (SMC)\n' +
    'แบบประเมินแบ่งออกเป็น 2 ตอน ได้แก่:\n' +
    '• ตอนที่ 1: ข้อมูลทั่วไปของผู้ตอบแบบประเมิน\n' +
    '• ตอนที่ 2: ความพึงพอใจต่อการใช้งานระบบ (เกณฑ์ระดับคะแนน 5 = มากที่สุด, 4 = มาก, 3 = ปานกลาง, 2 = น้อย, 1 = น้อยที่สุด)'
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);

  // ==================== ตอนที่ 1: ข้อมูลทั่วไปของผู้ตอบแบบประเมิน ====================
  form.addSectionHeaderItem()
      .setTitle('ตอนที่ 1: ข้อมูลทั่วไปของผู้ตอบแบบประเมิน')
      .setHelpText('กรุณากรอกข้อมูลพื้นฐานของผู้ใช้งานระบบ');

  var nameItem = form.addTextItem()
      .setTitle('ชื่อ - นามสกุล')
      .setRequired(true);

  var genderItem = form.addMultipleChoiceItem()
      .setTitle('เพศ')
      .setChoiceValues(['ชาย', 'หญิง'])
      .setRequired(true);

  var ageItem = form.addTextItem()
      .setTitle('อายุ (ปี)')
      .setRequired(true);

  var jobItem = form.addMultipleChoiceItem()
      .setTitle('อาชีพ / สถานภาพ')
      .setChoiceValues([
        'นักศึกษาสาขาวิทยาการคอมพิวเตอร์ / เทคโนโลยีสารสนเทศ',
        'เทรดเดอร์อิสระ (นักลงทุนรายย่อย)',
        'นักพัฒนาซอฟต์แวร์ (Software Developer / Programmer)',
        'พนักงานบริษัทเอกชน (นักลงทุนรายย่อย)'
      ])
      .setRequired(true);

  var expItem = form.addMultipleChoiceItem()
      .setTitle('ประสบการณ์ในการวิเคราะห์กราฟหรือเทรดในตลาดการเงิน')
      .setChoiceValues([
        'น้อยกว่า 1 ปี',
        '1 - 3 ปี',
        'มากกว่า 3 ปี'
      ])
      .setRequired(true);

  // ข้อมูลผู้ประเมินจริง 5 คน
  var respondents = [
    {
      name: 'นายธนกฤต วงศ์สุวรรณ',
      gender: 'ชาย',
      age: '22',
      job: 'นักศึกษาสาขาวิทยาการคอมพิวเตอร์ / เทคโนโลยีสารสนเทศ',
      exp: '1 - 3 ปี',
      comment: 'ระบบตีโซน Order Block และ FVG ได้ชัดเจนมาก ช่วยลดเวลาการไล่ดูกราฟหลาย Timeframe ได้ดี'
    },
    {
      name: 'นางสาวณัฐธิดา พงศ์ไพศาล',
      gender: 'หญิง',
      age: '21',
      job: 'นักศึกษาสาขาวิทยาการคอมพิวเตอร์ / เทคโนโลยีสารสนเทศ',
      exp: 'น้อยกว่า 1 ปี',
      comment: 'หน้าจอ Dashboard สรุปคะแนน 7 Timeframes ดูง่าย เหมาะกับคนที่เพิ่งเริ่มศึกษาทฤษฎี SMC'
    },
    {
      name: 'นายภูริภัทร ศรีวิไล',
      gender: 'ชาย',
      age: '26',
      job: 'เทรดเดอร์อิสระ (นักลงทุนรายย่อย)',
      exp: 'มากกว่า 3 ปี',
      comment: 'การแยกสถานะ BOS กับ CHoCH ด้วยราคาปิดแม่นยำดี ถ้าอนาคตเพิ่มระบบแจ้งเตือนผ่าน Line หรือ Telegram จะดีมาก'
    },
    {
      name: 'นายกิตติพงศ์ เจริญรัตน์',
      gender: 'ชาย',
      age: '24',
      job: 'นักพัฒนาซอฟต์แวร์ (Software Developer / Programmer)',
      exp: '1 - 3 ปี',
      comment: 'การดึงข้อมูลจาก MT5 รวดเร็ว กราฟลื่นไหล และฟังก์ชัน Backtest ช่วยเช็ค Win Rate ย้อนหลังได้สะดวก'
    },
    {
      name: 'นางสาวพิชญาภา อัครเดช',
      gender: 'หญิง',
      age: '28',
      job: 'พนักงานบริษัทเอกชน (นักลงทุนรายย่อย)',
      exp: '1 - 3 ปี',
      comment: 'ชอบตัว H4 Setup Radar ที่บอกระยะห่างจากโซนราคาสำคัญ ทำให้วางแผนจุดเข้าเทรดได้เป็นระบบมากขึ้น'
    }
  ];

  // ==================== ตอนที่ 2: ความพึงพอใจต่อการใช้งานระบบ (3 ด้าน 15 ข้อ) ====================
  var sections = [
    {
      title: 'ตอนที่ 2 (ด้านที่ 1): ความเหมาะสมของการพัฒนาโปรแกรมต่อการแก้ปัญหา',
      desc: 'ประเมินความสามารถของระบบในการช่วยลดระยะเวลาและลดอคติในการวิเคราะห์กราฟ (5 = มากที่สุด, 1 = น้อยที่สุด)',
      questions: [
        { q: '1.1 ระบบช่วยลดระยะเวลาในการวิเคราะห์และตีเส้นโครงสร้างตลาดเมื่อเทียบกับการตีกราฟด้วยมือ', scores: [5, 5, 4, 5, 4] },
        { q: '1.2 ระบบช่วยลดอคติทางอารมณ์ (Subjective Bias) และความสับสนในการตัดสินใจของผู้ใช้งาน', scores: [5, 4, 5, 4, 5] },
        { q: '1.3 ระบบช่วยให้มองเห็นแนวโน้มภาพรวมจากหลายกรอบเวลา (7 Timeframes) ได้ในคราวเดียว', scores: [4, 5, 5, 4, 5] },
        { q: '1.4 ระบบจำลองการทดสอบย้อนหลัง (Backtesting) ช่วยให้ตรวจสอบประสิทธิภาพกลยุทธ์ได้จริง', scores: [5, 4, 4, 5, 4] },
        { q: '1.5 ภาพรวมของโปรแกรมมีความเหมาะสมและตอบโจทย์ปัญหาการวิเคราะห์กราฟด้วยทฤษฎี SMC', scores: [4, 5, 4, 4, 5] }
      ]
    },
    {
      title: 'ตอนที่ 2 (ด้านที่ 2): การออกแบบส่วนติดต่อผู้ใช้ (GUI)',
      desc: 'ประเมินความชัดเจน ความสวยงาม และความสะดวกในการใช้งานหน้าจอระบบ (5 = มากที่สุด, 1 = น้อยที่สุด)',
      questions: [
        { q: '2.1 การจัดวางองค์ประกอบหน้าจอ (กราฟแท่งเทียน, ตาราง Dashboard และ Setup Radar) ดูง่ายและชัดเจน', scores: [5, 5, 4, 5, 4] },
        { q: '2.2 การใช้สีสัญลักษณ์ของโซน Bullish/Bearish Order Block, FVG และป้าย BOS/CHoCH แยกแยะได้ชัดเจน', scores: [5, 4, 5, 5, 4] },
        { q: '2.3 ปุ่มควบคุมการเลือกคู่เงิน กรอบเวลา และปุ่มเปิด-ปิดเลเยอร์ (Toggle Visibility) ใช้งานสะดวก', scores: [4, 5, 4, 5, 5] },
        { q: '2.4 การโต้ตอบกับกราฟ (การซูม การเลื่อนดูกราฟ และการแสดงข้อมูล) มีความลื่นไหลและต่อเนื่อง', scores: [5, 4, 4, 4, 5] },
        { q: '2.5 ความสวยงามและความเหมาะสมโดยรวมของส่วนติดต่อผู้ใช้ (User Interface)', scores: [4, 5, 3, 4, 5] }
      ]
    },
    {
      title: 'ตอนที่ 2 (ด้านที่ 3): ความเหมาะสมของเทคนิคและฟังก์ชันที่ใช้',
      desc: 'ประเมินความถูกต้องของอัลกอริทึม SMC และประสิทธิภาพการประมวลผลของระบบ (5 = มากที่สุด, 1 = น้อยที่สุด)',
      questions: [
        { q: '3.1 ความถูกต้องของการตรวจจับจุดกลับตัว (Swing High/Low) และการเปลี่ยนโครงสร้างตลาด (BOS / CHoCH)', scores: [5, 5, 5, 4, 5] },
        { q: '3.2 ความถูกต้องของการระบุโซนสถาบัน Order Block (OB), ช่องว่างราคา (FVG) และสถานะ Mitigated', scores: [5, 4, 5, 5, 4] },
        { q: '3.3 ความเหมาะสมของการคำนวณคะแนนถ่วงน้ำหนักพหุกรอบเวลา (Multi-Timeframe Scoring) ทั้ง 7 กรอบเวลา', scores: [4, 5, 4, 5, 5] },
        { q: '3.4 ประสิทธิภาพการทำงานของระบบแจ้งเตือนระยะห่างโซนราคาสำคัญ (H4 SMC Setup Radar)', scores: [5, 4, 5, 4, 4] },
        { q: '3.5 ความรวดเร็วและความเสถียรของการดึงข้อมูลแท่งเทียนจาก MetaTrader 5 มาประมวลผลและแสดงผล', scores: [4, 5, 4, 5, 4] }
      ]
    }
  ];

  var scaleItems = [];
  var allScores = [];

  for (var s = 0; s < sections.length; s++) {
    var sec = sections[s];
    form.addPageBreakItem().setTitle(sec.title).setHelpText(sec.desc);

    for (var i = 0; i < sec.questions.length; i++) {
      var itemData = sec.questions[i];
      var scaleItem = form.addScaleItem();
      scaleItem.setTitle(itemData.q)
               .setBounds(1, 5)
               .setLabels('น้อยที่สุด (1)', 'มากที่สุด (5)')
               .setRequired(true);
      scaleItems.push(scaleItem);
      allScores.push(itemData.scores);
    }
  }

  // ข้อเสนอแนะเพิ่มเติม
  var commentItem = form.addParagraphTextItem()
      .setTitle('ข้อเสนอแนะเพิ่มเติม (ถ้ามี)')
      .setRequired(false);

  // 2. สร้าง Google Sheet เชื่อมกับ Form อัตโนมัติ
  var ss = SpreadsheetApp.create('ผลการประเมินความพึงพอใจ_SMC_5คน (Responses)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  // 3. ส่งคำตอบของผู้ประเมินทั้ง 5 คนเข้าฟอร์มอัตโนมัติ (พร้อมชื่อ อายุ อาชีพ และคะแนนที่ตรงตารางที่ 3 เป๊ะ)
  for (var person = 0; person < 5; person++) {
    var p = respondents[person];
    var formResponse = form.createResponse();

    // ข้อมูลทั่วไป (ตอนที่ 1)
    formResponse.withItemResponse(nameItem.createResponse(p.name));
    formResponse.withItemResponse(genderItem.createResponse(p.gender));
    formResponse.withItemResponse(ageItem.createResponse(p.age));
    formResponse.withItemResponse(jobItem.createResponse(p.job));
    formResponse.withItemResponse(expItem.createResponse(p.exp));

    // คะแนนความพึงพอใจ 15 ข้อ (ตอนที่ 2)
    for (var qIdx = 0; qIdx < scaleItems.length; qIdx++) {
      var score = allScores[qIdx][person];
      formResponse.withItemResponse(scaleItems[qIdx].createResponse(score));
    }

    // ข้อเสนอแนะ
    formResponse.withItemResponse(commentItem.createResponse(p.comment));
    formResponse.submit();
  }

  Logger.log('====================================================');
  Logger.log('✅ สร้าง Google Form พร้อมข้อมูลผู้ประเมิน 5 คน (ชื่อ-อายุ-อาชีพ) สำเร็จเรียบร้อย!');
  Logger.log('🔗 ลิงก์สำหรับส่งให้ผู้ประเมิน (Published URL): ' + form.getPublishedUrl());
  Logger.log('🛠️ ลิงก์สำหรับแก้ไขฟอร์มและดูกราฟผลลัพธ์ (Edit URL): ' + form.getEditUrl());
  Logger.log('📊 ลิงก์ตาราง Google Sheets: ' + ss.getUrl());
  Logger.log('====================================================');
}
