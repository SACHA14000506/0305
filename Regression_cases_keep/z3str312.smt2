(set-logic QF_S)

(declare-fun sigmaStar_0 () String)
(declare-fun sigmaStar_1 () String)
(declare-fun sigmaStar_2 () String)
(declare-fun literal_8 () String)
(declare-fun x_9 () String)
(declare-fun literal_3 () String)
(declare-fun x_10 () String)
(declare-fun literal_11 () String)
(declare-fun x_12 () String)
(declare-fun x_13 () Int)
(declare-fun x_14 () Int)
(declare-fun x_15 () String)
(declare-fun x_16 () String)
(declare-fun x_17 () String)
(declare-fun x_18 () Int)
(declare-fun x_19 () String)
(declare-fun x_20 () String)
(declare-fun x_21 () Int)

(assert (= literal_8 "\x69\x6e\x63\x6c\x75\x64\x65\x2f\x6c\x61\x6e\x67\x2f"))
(assert (= literal_3 "\x65\x6e"))
(assert (or (= x_9 sigmaStar_2) (= x_9 literal_3) (= x_9 sigmaStar_1) (= x_9 sigmaStar_0)))
(assert (= x_10 (str.++ literal_8 x_9)))
(assert (= literal_11 "\x2f\x73\x65\x6e\x64\x63\x61\x72\x64\x2e\x6c\x61\x6e\x67\x2e\x70\x68\x70"))
(assert (= x_12 (str.++ x_10 literal_11)))
(assert (= x_13 (str.len x_12)))
(assert (> x_13 10))
(assert (str.contains x_12 "\x6c\x61\x6e\x67"))
(assert (str.prefixof literal_8 x_10))
(assert (str.suffixof literal_11 x_12))
(assert (= x_14 (str.indexof x_12 "\x65" 0)))
(assert (>= x_14 0))
(assert (= x_15 (str.replace x_12 "\x65" "\x45")))
(assert (= x_16 (str.substr x_15 0 5)))
(assert (= x_17 (str.at x_12 5)))
(assert (= x_18 (str.to.int x_17)))
(assert (= x_19 (str.substr x_12 10 5)))
(assert (= x_20 (str.++ x_19 "\x2f\x65\x76\x69\x6c")))
(assert (= x_21 (str.indexof x_20 "\x6c" 0)))
(assert (>= x_21 0))
(assert (str.in-re x_12 (re.++ (re.* re.allchar) (re.++ (str.to-re "\x2f\x65\x76\x69\x6c") (re.* re.allchar)))))

(check-sat)
(exit)