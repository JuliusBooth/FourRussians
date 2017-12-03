import java.util.Arrays;

/**
 * Created by mohsenkatebi on 2017-11-30.
 */
public class OffsetFunctionInput {
    private String s1, s2;
    private int[] v1, v2;
    public String hStr;
    private int hHashCode;

    public OffsetFunctionInput(int[] s1Vector, int[] s2Vector, int[] v1, int[] v2) {
        this.v1 = Arrays.copyOf(v1, v1.length);
        this.v2 = Arrays.copyOf(v2, v2.length);
        buildH(s1Vector, s2Vector, v1, v2);
    }

    public OffsetFunctionInput(String s1, String s2, int[] v1, int[] v2) {
        this.v1 = Arrays.copyOf(v1, v1.length);
        this.v2 = Arrays.copyOf(v2, v2.length);
        this.s1 = s1;
        this.s2 = s2;
        buildH(v1, v2);
    }

    public String getS1() {
        return s1;
    }

    public String getS2() {
        return s2;
    }

    public int[] getV2() {
        return v2;
    }

    public int[] getV1() {
        return v1;
    }

    private StringBuilder getStr(int[] strVector) {
        StringBuilder str = new StringBuilder(strVector.length);
        for (int aStrVector : strVector) {
            str.append(FourRussiansSpeedup.alpha[aStrVector]);
        }
        return str;
    }

    private StringBuilder getOffsetStr(int[] offsetVector) {
        StringBuilder str = new StringBuilder(offsetVector.length);
        for (int aStrVector : offsetVector) {
            str.append(aStrVector + 1);
        }
        return str;
    }

    private void buildH(int[] V1, int[] V2) {
        StringBuilder h = new StringBuilder(s1);
        h.append("#");
        h.append(s2);
        h.append("#");
        h.append(getOffsetStr(V1));
        h.append("#");
        h.append(getOffsetStr(V2));
        hStr = h.toString();
        hHashCode = hStr.hashCode();
    }

    private void buildH(int[] S1, int[] S2, int[] V1, int[] V2) {
        StringBuilder s1h = getStr(S1);
        StringBuilder s2h = getStr(S2);
        this.s1 = s1h.toString();
        this.s2 = s2h.toString();
        s1h.append("#");
        s1h.append(s2h);
        s1h.append("#");
        s1h.append(getOffsetStr(V1));
        s1h.append("#");
        s1h.append(getOffsetStr(V2));
        hStr = s1h.toString();
        hHashCode = hStr.hashCode();
    }

    @Override
    public boolean equals(Object o) {
        if (o instanceof OffsetFunctionInput) {
            OffsetFunctionInput other = (OffsetFunctionInput) o;
            return this.hStr.equals(other.hStr);
        }
        return false;
    }

    @Override
    public int hashCode() {
        return this.hHashCode;
    }

}
