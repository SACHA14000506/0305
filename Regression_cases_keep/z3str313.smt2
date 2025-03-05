(set-logic QF_S)

(declare-fun sigmaStar_0 () String)
(declare-fun literal_1 () String)
(declare-fun x_2 () String)
(declare-fun literal_3 () String)
(declare-fun x_4 () String)
(declare-fun x_5 () String)
(declare-fun x_6 () String)

(assert (= literal_1 "\x3c\x74\x64\x20\x77\x69\x64\x74\x68\x3d\x27\x31\x25\x27\x20\x63\x6c\x61\x73\x73\x3d\x27\x74\x62\x6c\x32\x27\x20\x73\x74\x79\x6c\x65\x3d\x27\x77\x68\x69\x74\x65\x2d\x73\x70\x61\x63\x65\x3a\x6e\x6f\x77\x72\x61\x70\x27\x3e"))
(assert (= x_2 (str.++ literal_1 sigmaStar_0)))
(assert (= literal_3 "\x3c\x2f\x74\x64\x3e\x5c\x6e\x3c\x2f\x74\x72\x3e\x5c\x6e"))
(assert (= x_4 (str.++ x_2 literal_3)))
(assert (str.in-re x_4 (re.++ (re.* re.allchar) (re.++ (str.to-re "\x5c\x3c\x53\x43\x52\x49\x50\x54") (re.* re.allchar)))))

(assert (= x_5 (str.replace x_4 "\x5c\x6e" " ")))
(assert (= x_6 (str.substr x_5 0 (str.indexof x_5 "\x5c\x3c\x53\x43\x52\x49\x50\x54" 0))))

(assert (str.contains x_6 "\x77\x68\x69\x74\x65\x2d\x73\x70\x61\x63\x65"))
(assert (str.prefixof "\x3c\x74\x64" x_6))
(assert (str.suffixof "\x3e" x_6))
(assert (= (str.len x_6) 100))

(check-sat)
(exit)