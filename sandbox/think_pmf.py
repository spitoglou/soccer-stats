import external.thinkplot as thinkplot
import external.thinkstats2 as thinkstats2
from sp_soccer_lib import no_draw_frequencies


def main():

    freq1 = no_draw_frequencies('greece', ['Olympiakos'])
    freq2 = no_draw_frequencies('greece', ['AEK'])
    print(freq1, freq2)
    width = 0.45
    first_hist = thinkstats2.Hist(freq1, label='Olympiakos')
    other_hist = thinkstats2.Hist(freq2, label='AEK')

    '''
    thinkplot.PrePlot takes the number of histograms we are planning to plot;
    it uses this information to choose an appropriate collection of colors.
    '''

    thinkplot.PrePlot(2)
    thinkplot.Hist(first_hist, align='right', width=width)
    thinkplot.Hist(other_hist, align='left', width=width)
    thinkplot.Show(xlabel='no_draw_streaks', ylabel='frequency')
    # thinkplot.Show(xlabel='weeks', ylabel='frequency', xlim=[27, 46])

    '''
    Another way to represent a distribution is a probability mass function
    (PMF), which maps from each value to its probability. A probability is a
    frequency expressed as a fraction of the sample size, n. To get from frequen-
    cies to probabilities, we divide through by n, which is called normalization.
    '''

    freq_greece = no_draw_frequencies('greece')
    freq_england = no_draw_frequencies('england')
    pmf = thinkstats2.Pmf(freq_greece, label='Greece')
    pmf2 = thinkstats2.Pmf(freq_england, label='England')
    print(pmf)

    print(pmf.Prob(2))

    '''
    The Pmf is normalized so total probability is 1.
    Pmf and Hist objects are similar in many ways; in fact, they inherit many
    of their methods from a common parent class. For example, the methods
    Values and Items work the same way for both. The biggest difference is
    that a Hist maps from values to integer counters; a Pmf maps from values
    to floating-point probabilities.
    To look up the probability associated with a value, use Prob:
    >>> pmf.Prob(2)
    0.4
    The bracket operator is equivalent:
    >>> pmf[2]
    0.4
    You can modify an existing Pmf by incrementing the probability associated
    with a value:
    >>> pmf.Incr(2, 0.2)
    >>> pmf.Prob(2)
    0.6
    Or you can multiply a probability by a factor:
    >>> pmf.Mult(2, 0.5)
    >>> pmf.Prob(2)
    0.3
    If you modify a Pmf, the result may not be normalized; that is, the probabil-
    ities may no longer add up to 1. To check, you can call Total, which returns
    the sum of the probabilities:
    >>> pmf.Total()
    0.9
    To renormalize, call Normalize:
    >>> pmf.Normalize()
    >>> pmf.Total()
    1.0
    Pmf objects provide a Copy method so you can make and modify a copy
    without affecting the original.
    '''

    thinkplot.PrePlot(2)
    # thinkplot.SubPlot(2)
    thinkplot.Pmfs([pmf, pmf2])
    thinkplot.Show(xlabel='no_draw_streaks')

    countries = ['greece', 'italy', 'england', 'spain', 'germany', 'france']
    freqs = []
    pmfs = []
    for country in countries:
        thinkplot.PrePlot(len(countries))
        # freqs.append(no_draw_frequencies(country))
        pmfs.append(thinkstats2.Pmf(
            no_draw_frequencies(country), label=country))
    thinkplot.Pmfs(pmfs)
    thinkplot.Show(xlabel='no_draw_streaks')
