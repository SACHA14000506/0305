(set-logic QF_S)
(declare-fun sigmaStar_0 () String)
(declare-fun sigmaStar_1 () String)
(declare-fun literal_2 () String)
(declare-fun x_3 () String)
(declare-fun literal_4 () String)
(declare-fun x_5 () String)
(declare-fun literal_8 () String)
(declare-fun x_9 () String)
(declare-fun literal_7 () String)
(declare-fun x_10 () String)

(assert (= literal_2 "\x2f\x6c\x61\x6e\x67\x2f"))
(assert (= x_3 (str.++ literal_2 sigmaStar_0)))
(assert (= literal_4 "\x5f\x6c\x6f\x63\x61\x6c"))
(assert (= x_5 (str.++ x_3 literal_4)))
(assert (= literal_8 "\x2f"))
(assert (= x_9 (str.++ x_5 literal_8)))
(assert (= literal_7 "\x63\x75\x72\x72\x65\x6e\x74\x66\x69\x6c\x65"))
(assert (= x_10 (str.++ x_9 literal_7)))
(assert (str.contains x_10 "\x2f\x65\x76\x69\x6c"))
(assert (str.prefixof literal_2 x_10))
(assert (str.suffixof literal_7 x_10))
(assert (> (str.len x_10) 10))
(assert (>= (str.indexof x_10 "\x5f\x6c\x6f\x63\x61\x6c" 0) 0))
(assert (= (str.substr x_10 0 6) literal_2))
(assert (= (str.at x_10 0) "\x2f"))
(assert (not (= (str.replace x_10 "\x5f\x6c\x6f\x63\x61\x6c" "\x4c\x6f\x63\x61\x6c") x_10)))
(assert (< (str.to.int x_10) 0))
(assert (= (str.++ x_10 (int.to.str (str.to.int x_10))) x_10))
(assert (str.in-re x_10 (re.++ (re.* re.allchar) (re.++ (str.to-re "\x2f\x65\x76\x69\x6c") (re.* re.allchar)))))
(check-sat)
(exit)