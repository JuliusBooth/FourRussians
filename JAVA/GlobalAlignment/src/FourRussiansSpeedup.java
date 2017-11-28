import java.util.Arrays;
import java.util.HashMap;
import java.util.Objects;

public class FourRussiansSpeedup {

    public static char[] alpha = {'a', 'c', 'g', 't'};
    private String firstSeq, secondSeq;
    private int t;

    private void preProcess() {
        int[] wordVector1 = new int[t];
        int[] wordVector2 = new int[t];
        do {
            do {
                int[] offsetVector1 = new int[t];
                int[] offsetVector2 = new int[t];
            }
            while (nextWordVector(wordVector2) == 0);
        } while (nextWordVector(wordVector1) == 0);
    }

    private int nextWordVector(int[] current) {
        for (int i = 0; i < current.length; i++) {
            if (current[i] < 3) {
                current[i]++;
                return 0;
            } else {
                current[i] = 0;
            }
        }
        return 1;
    }
}

class BlockFunctionArgs {
    private int[] s1Vector, s2Vector;
    private int[] v1, v2;
    private String hStr;
    private int hHashCode;

    public BlockFunctionArgs(int[] s1Vector, int[] s2Vector, int[] v1, int[] v2) {
        this.s1Vector = Arrays.copyOf(s1Vector, s1Vector.length);
        this.s2Vector = Arrays.copyOf(s2Vector, s2Vector.length);
        this.v1 = Arrays.copyOf(v1, v1.length);
        this.v2 = Arrays.copyOf(v2, v2.length);
        buildH(s1Vector, s2Vector, v1, v2);
    }

    private StringBuilder getStr(int[] strVector) {
        StringBuilder str = new StringBuilder(strVector.length);
        for (int aStrVector : strVector) {
            str.append(FourRussiansSpeedup.alpha[aStrVector]);
        }
        return str;
    }

    private void buildH(int[] S1, int[] S2, int[] V1, int[] V2) {
        StringBuilder h = getStr(S1);
        h.append("#");
        h.append(getStr(S2));
        h.append("#");
        h.append(getStr(V1));
        h.append("#");
        h.append(getStr(V2));
        hStr = h.toString();
        hHashCode = hStr.hashCode();
    }

    @Override
    public boolean equals(Object o) {
        if (o instanceof BlockFunctionArgs) {
            BlockFunctionArgs other = (BlockFunctionArgs) o;
            return this.hStr.equals(other.hStr);
        }
        return false;
    }

    @Override
    public int hashCode() {
        return this.hHashCode;
    }
}
