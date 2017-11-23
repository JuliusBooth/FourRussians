/**
 * Created by mohsenkatebi on 2017-11-23.
 */
public class StandardGlobalAlignment {

    public static void main(String[] args) {
        StandardGlobalAlignment sga = new StandardGlobalAlignment();
        sga.init("AAGTGCA", "ACGTTC", 1, 0, 1);
        System.out.println(sga.getOptimalCost());
        sga.printCostMatrix();
        String[] optimalAlignment = sga.getOptimalAlignment();
        System.out.println(optimalAlignment[0]);
        System.out.println(optimalAlignment[1]);
        sga.printTraceMatrix();
    }

    private static final String GAP = "-";
    private int[][] costs;
    private int[][] traces;
    private String firstSeq;
    private String secondSeq;
    private String[] optimalAlignment;
    private int n, m;
    private int gapCost, matchCost, mismatchCost;

    public void printCostMatrix() {
        printMatrix(costs, n, m);
    }

    public void printTraceMatrix() {
        printMatrix(traces, n, m);
    }

    private void printMatrix(int[][] matrix, int n, int m) {
        for (int i = 0; i <= n; i++) {
            for (int j = 0; j <= m; j++) {
                System.out.printf("%2d ", matrix[i][j]);
            }
            System.out.println();
        }
    }

    private int getGapCost() {
        return gapCost;
    }

    private int getMatchCost() {
        return matchCost;
    }

    private int getMismatchCost() {
        return mismatchCost;
    }

    private void setGapCost(int gapCost) {
        this.gapCost = gapCost;
    }

    private void setMatchCost(int matchCost) {
        this.matchCost = matchCost;
    }

    private void setMismatchCost(int mismatchCost) {
        this.mismatchCost = mismatchCost;
    }

    public void init(String firstSeq, String secondSeq, int gapCost, int matchCost, int mismatchCost) {
        setFirstSeq(firstSeq);
        setSecondSeq(secondSeq);
        setGapCost(gapCost);
        setMatchCost(matchCost);
        setMismatchCost(mismatchCost);
        this.costs = new int[n + 1][m + 1];
        this.traces = new int[n + 1][m + 1];
        this.optimalAlignment = new String[2];
    }

    private void setCost(int i, int j, int cost) {
        this.costs[i][j] = cost;
    }

    private int getCost(int i, int j) {
        return costs[i][j];
    }

    private void setTrace(int i, int j, int trace) {
        this.traces[i][j] = trace;
    }

    private int getTrace(int i, int j) {
        return traces[i][j];
    }

    private String getFirstSeq() {
        return firstSeq;
    }

    private void setFirstSeq(String firstSeq) {
        this.firstSeq = firstSeq;
        this.n = firstSeq.length();
    }

    private String getSecondSeq() {
        return secondSeq;
    }

    private void setSecondSeq(String secondSeq) {
        this.secondSeq = secondSeq;
        this.m = secondSeq.length();
    }

    public int getOptimalCost() {
        if (getTrace(n, m) == 0) {
            doAlignment();
        }
        return getCost(n , m);
    }

    private void doAlignment() {
        setCost(0, 0, 0);
        for (int i = 1; i <= n; i++) {
            setCost(i, 0, getCost(i - 1, 0) + getGapCost());
            setTrace(i, 0, 3);
        }
        for (int j = 1; j <= m; j++) {
            setCost(0, j, getCost(0, j - 1) + getGapCost());
            setTrace(0, j, 2);
        }
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                int d = getFirstSeq().charAt(i - 1) == getSecondSeq().charAt(j - 1) ? getMatchCost() : getMismatchCost();
                int c = getCost(i - 1, j - 1) + d;
                int t = 1;
                int upC = getCost(i, j - 1) + getGapCost();
                if (c > upC) {
                    c = upC;
                    t = 2;
                }
                int leftC = getCost(i - 1, j) + getGapCost();
                if (c > leftC) {
                    c = leftC;
                    t = 3;
                }
                setCost(i, j, c);
                setTrace(i, j, t);
            }
        }
    }

    public String[] getOptimalAlignment() {
        if (optimalAlignment[0] == null) {
            backtrack();
        }
        return optimalAlignment;
    }

    private void backtrack() {
        if (getTrace(n, m) == 0) {
            doAlignment();
        }
        StringBuilder first = new StringBuilder();
        StringBuilder second = new StringBuilder();
        int i = n;
        int j = m;
        while (i > 0 || j > 0) {
            switch (getTrace(i, j)) {
                case 1: {
                    first.append(this.firstSeq.charAt(i - 1));
                    second.append(this.secondSeq.charAt(j - 1));
                    i--;
                    j--;
                    break;
                }
                case 2: {
                    second.append(this.secondSeq.charAt(j - 1));
                    first.append(GAP);
                    j--;
                    break;
                }
                case 3: {
                    first.append(this.firstSeq.charAt(i - 1));
                    second.append(GAP);
                    i--;
                    break;
                }
            }
        }
        optimalAlignment[0] = first.reverse().toString();
        optimalAlignment[1] = second.reverse().toString();
    }
}
