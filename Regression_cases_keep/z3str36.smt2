(set-logic QF_S)
(declare-fun sigmaStar_0 () String)
(declare-fun sigmaStar_1 () String)
(declare-fun sigmaStar_2 () String)
(declare-fun sigmaStar_3 () String)
(declare-fun sigmaStar_4 () String)
(declare-fun sigmaStar_8 () String)
(declare-fun literal_7 () String)
(declare-fun x_10 () String)
(declare-fun sigmaStar_12 () String)
(declare-fun literal_11 () String)
(declare-fun x_13 () String)
(declare-fun x_14 () String)
(declare-fun literal_15 () String)
(declare-fun x_16 () String)
(declare-fun x_9 () String)
(assert (= x_9 (str.replace sigmaStar_0 "\x2c" "\x20")))
(assert (= literal_7 "\x3c\x74\x72\x3e\x0d\x0a\x3c\x74\x64\x20\x77\x69\x64\x74\x68\x3d\x27\x31\x34\x35\x27\x20\x63\x6c\x61\x73\x73\x3d\x27\x74\x62\x6c\x32\x27\x3e"))
(assert (= x_10 (str.++ literal_7 sigmaStar_1)))
(assert (= literal_11 "\x3c\x2f\x74\x64\x3e\x0d\x0a\x3c\x74\x64\x20\x63\x6c\x61\x73\x73\x3d\x27\x74\x62\x6c\x31\x27\x3e\x3c\x69\x6e\x70\x75\x74\x20\x74\x79\x70\x65\x3d\x27\x66\x69\x6c\x65\x27\x20\x6e\x61\x6d\x65\x3d\x27\x61\x74\x74\x61\x63\x68\x27\x20\x65\x6e\x63\x74\x79\x70\x65\x3d\x27\x6d\x75\x6c\x74\x69\x70\x61\x72\x74\x2f\x66\x6f\x72\x6d\x2d\x64\x61\x74\x61\x27\x20\x63\x6c\x61\x73\x73\x3d\x27\x74\x65\x78\x74\x62\x6f\x78\x27\x20\x73\x74\x79\x6c\x65\x3d\x27\x77\x69\x64\x74\x68\x3a\x32\x30\x30\x70\x78\x3b\x27\x3e\x3c\x62\x72\x3e\x0d\x0a\x3c\x73\x70\x61\x6e\x20\x63\x6c\x61\x73\x73\x3d\x27\x73\x6d\x61\x6c\x6c\x32\x27\x3e"))
(assert (= x_13 (str.++ x_10 literal_11)))
(assert (= x_14 (str.++ x_13 sigmaStar_12)))
(assert (= literal_15 "\x3c\x2f\x73\x70\x61\x6e\x3e\x3c\x2f\x74\x64\x3e\x0d\x0a\x3c\x2f\x74\x72\x3e\x5c\x6e"))
(assert (= x_16 (str.++ x_14 literal_15)))
(assert (str.contains x_16 "\x3c\x74\x72\x3e"))
(assert (str.prefixof "\x3c\x74\x72\x3e" x_16))
(assert (str.suffixof "\x5c\x6e" x_16))
(assert (> (str.indexof x_16 "\x3c\x2f\x74\x64\x3e") 0))
(assert (= (str.len x_16) (+ (str.len x_14) (str.len literal_15))))
(assert (str.in-re x_16 (re.++ (re.* re.allchar) (re.++ (str.to-re "\x5c\x3c\x53\x43\x52\x49\x50\x54") (re.* re.allchar)))))
(check-sat)
(exit)