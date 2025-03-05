(set-logic QF_S)
(declare-fun sigmaStar_0 () String)
(declare-fun literal_1 () String)
(declare-fun x_2 () String)
(assert (= literal_1 "\x5c\x6e"))
(assert (= x_2 (str.++ sigmaStar_0 literal_1)))
(assert (str.in-re x_2 (re.++ (re.* re.allchar) (re.++ (str.to-re "\x5c\x3c\x53\x43\x52\x49\x50\x54") (re.* re.allchar)))))
(assert (str.contains x_2 "\x5c\x6e"))
(assert (= (str.len x_2) (+ (str.len sigmaStar_0) (str.len literal_1))))
(assert (str.prefixof sigmaStar_0 x_2))
(assert (str.suffixof literal_1 x_2))
(assert (= (str.indexof x_2 literal_1) (str.len sigmaStar_0)))
(assert (= (str.substr x_2 (str.len sigmaStar_0) (str.len literal_1)) literal_1))
(assert (= (str.replace x_2 literal_1 "\x5c\x6e\x5c\x6e") (str.++ sigmaStar_0 "\x5c\x6e\x5c\x6e")))
(assert (= (str.at x_2 (str.len sigmaStar_0)) "\x5c"))
(assert (= (str.to.int (str.substr x_2 (str.len sigmaStar_0) (str.len literal_1))) (str.to.int literal_1)))
(assert (= (int.to.str (str.len x_2)) (int.to.str (+ (str.len sigmaStar_0) (str.len literal_1)))))
(check-sat)
(exit)