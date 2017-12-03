import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;

public class FourRussiansSpeedup {

    public static char[] alpha = {'A', 'C', 'G', 'T'};
    private String firstSeq, secondSeq;
    private int n, m, nk, mk;
    private int t;
    private HashMap<OffsetFunctionInput, OffsetFunctionOutput> precomputedBlocks;
    private TBlock[][] blocks;
    private int optimalCost;
    private StandardGlobalAlignment sga;

    private static String randormGen(int size) {
        StringBuilder s = new StringBuilder(size);
        for (int i = 0; i < size; i++) {
            Random randGen = new Random();
            int rand = randGen.nextInt(4);
            s.append(alpha[rand]);
        }
        return s.toString();
    }

    public static void main(String[] args) {
        FourRussiansSpeedup frs = new FourRussiansSpeedup();
        String s1 = randormGen(1026);
        String s2 = randormGen(1026);
        frs.init(s1, s2);
        frs.doAlignment();
        System.out.println(frs.getOptimalCost());
        StandardGlobalAlignment standard = new StandardGlobalAlignment();
        standard.init(s1, s2, 1, 0, 1);
        System.out.println(standard.getOptimalCost());
//        frs.printBlocks();
//        System.out.println(sga.getOptimalCost());
//        sga.printCostMatrix();
//        String[] optimalAlignment = sga.getOptimalAlignment();
//        System.out.println(optimalAlignment[0]);
//        System.out.println(optimalAlignment[1]);
//        sga.printTraceMatrix();
    }

    private void printBlock(TBlock block) {
        for (int i = 0; i < t; i++) {
            for (int j = 0; j < t; j++) {
                if (i == 0 && j == 0) {
                    System.out.printf("%5d ", 0);
                } else if (i == 0) {
                    System.out.printf("%5d ", block.getOffsetRowFirst()[j - 1]);
                } else if (i == t - 1 && j != 0) {
                    if (j == t - 1) {
                        System.out.printf("%2d,%2d", block.getOffsetRowLast()[j - 1], block.getOffsetColLast()[i - 1]);
                    } else {
                        System.out.printf("%5d ", block.getOffsetRowLast()[j - 1]);
                    }
                } else {
                    if (j == 0) {
                        System.out.printf("%5d ", block.getOffsetColFirst()[i - 1]);
                    } else if (j == t - 1) {
                        System.out.printf("%5d", block.getOffsetColLast()[i - 1]);
                    } else {
                        System.out.printf("%5d ", 8);
                    }
                }
                if (j == t - 1) {
                    System.out.println();
                }
            }
        }
        System.out.println();
    }

    public void printBlocks() {
        for (int i = 0; i < nk; i++) {
            for (int j = 0; j < mk; j++) {
                System.out.println(i + "," + j);
                printBlock(blocks[i][j]);
            }
        }

    }

    public void init(String firstSeq, String secondSeq) {
        this.firstSeq = firstSeq;
        this.secondSeq = secondSeq;
        sga = new StandardGlobalAlignment();
        n = firstSeq.length();
        m = secondSeq.length();
        t = 9;
        nk = n / (t - 1);
        mk = m / (t - 1);
    }

    public void doAlignment() {
        preprocess();
        blocks = new TBlock[nk][mk];
        optimalCost = n;
        for (int i = 0; i < nk; i++) {
            for (int j = 0; j < mk; j++) {
                TBlock current = new TBlock(t);
                TBlock up = j > 0 ? blocks[i][j - 1] : null;
                TBlock left = i > 0 ? blocks[i - 1][j] : null;
                for (int it = 0; it < t - 1; it++) {
                    current.getOffsetRowFirst()[it] = up == null ? 1 : up.getOffsetRowLast()[it];
                    current.getOffsetColFirst()[it] = left == null ? 1 : left.getOffsetColLast()[it];
                }
                String s1 = firstSeq.substring((t - 1) * i, (t - 1) * (i + 1));
                String s2 = secondSeq.substring((t - 1) * j, (t - 1) * (j + 1));
                OffsetFunctionInput key = new OffsetFunctionInput(s1, s2, current.getOffsetRowFirst(), current.getOffsetColFirst());
                System.out.println(key.hStr);
                OffsetFunctionOutput value = precomputedBlocks.get(key);
                current.setOffsetRowLast(value.getV1());
                current.setOffsetColLast(value.getV2());
                blocks[i][j] = current;
            }
        }
        for (int j = 0; j < mk; j++) {
            for (int it = 0; it < t - 1; it++) {
                optimalCost += blocks[nk - 1][j].getOffsetColLast()[it];
            }
        }
    }

    public int getOptimalCost() {
        return optimalCost;
    }

    private void preprocess() {
        precomputedBlocks = new HashMap<>();
        int[] wordVector1 = new int[t - 1];
        int[] wordVector2 = new int[t - 1];
        do {
            do {
                int[] offsetVector1 = new int[t - 1];
                Arrays.fill(offsetVector1, -1);
                int[] offsetVector2 = new int[t - 1];
                Arrays.fill(offsetVector2, -1);
                do {
                    do {
                        OffsetFunctionInput in = new OffsetFunctionInput(wordVector1, wordVector2, offsetVector1, offsetVector2);
//                        System.out.println(in.hStr);
                        OffsetFunctionOutput out = offsetFunction(in);
                        precomputedBlocks.put(in, out);
                    } while (nextVector(offsetVector2, -1, 1) == 0);
                } while (nextVector(offsetVector1, -1, 1) == 0);
            } while (nextVector(wordVector2, 0, 3) == 0);
//            System.out.println("end 2");
//            for (int hh = 0; hh < wordVector1.length; hh++) {
//                System.out.println(wordVector1[hh]);
//            }
        } while (nextVector(wordVector1, 0, 3) == 0);
        System.out.println("end preprocess");
    }

    private OffsetFunctionOutput offsetFunction(OffsetFunctionInput input) {
        sga.init(input.getS1(), input.getS2(), 1, 0, 1, input.getV1(), input.getV2());
        sga.doAlignment();
        return sga.getOffsets();
    }

    private int nextVector(int[] current, int from, int to) {
        for (int i = 0; i < current.length; i++) {
            if (current[i] < to) {
                current[i]++;
                return 0;
            } else {
                current[i] = from;
            }
        }
        return 1;
    }
}
