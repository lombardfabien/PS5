# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name:
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    """ for each degree, generate a model and implement it in models"""
    #assert degs ==[]
    models =[]
    for deg in degs:
        model = pylab.polyfit(x,y,deg)
        models.append(model)
    """ return a list of models defined by the list of degs"""
    #print (models)
    return models
    pass

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.

    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    error = ((estimated - y)**2).sum()
    mean = y.sum() / len (y)
    variance = ((y - mean)**2).sum()
    #print ('error:', error, 'variance:', variance)
    return  1 - (error/variance)
    pass

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    pylab.plot(x,y,"ob", label = "data")
    for i in range (len(models)):
        y_estimate = pylab.polyval(models[i], x)
        R2 = r_squared(y, y_estimate)
        """if model is degree one or len of 2, se slope to be calculated"""
        if len(models[i])==2:
            se = se_over_slope(x, y, y_estimate, models[i])
            pylab.plot(x,y_estimate,"-r", label = "model " + str(i) + " R2: " + str(round(R2,5)) + " se slope: " + str(round(se,5)))
        #"""if other than 1 degre model, plot the curve without se slope"""
        else:
            pylab.plot(x,y,"ob", label = "data")
            pylab.plot(x,y_estimate,"-r", label = "model " + str(i) + " R2: " + str(round(R2,5)))
        pylab.xlabel("Year")
        pylab.ylabel("maximum temperature in Celsius")
        pylab.legend(loc ='best')
        pylab.title("average temperature over the years")
        pylab.show()

    #pass

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    nat_yearly_temp =[]
    xval_year = []
    for year in years:
        avg_temp_nat_day = []
        for city in multi_cities:
            avg_temp_nat_day.append(climate.get_yearly_temp(city, year).mean())
        nat_yearly_temp.append(pylab.array(avg_temp_nat_day).mean())
        #print (year, ": ", len(avg_temp_nat_year))
        #print("year", year, " national temperature: ", nat_yearly_temp)
    return pylab.array(nat_yearly_temp)



    pass

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    #print (y)
    moving_average_array = []
    i = 0
    while i < len(y):
        list_to_average = []
        window = i - window_length + 1
        index = 0
        sum = 0
        """ calculate moving average for early number """
        if window < 0:
            while index <= i:
                sum = y[index] + sum
                #print(sum)
                index+=1
            moving_average_array.append(sum/(index))
            #print ("first value:", window,"values to average:", y[index], "value index:", i, "length", index)

        else:
            """ calculate average included in the window lenght"""
            #print ("first value:", window,"last value:", i, "values to average:", y[window:i+1], "length", len(y[window:i+1]))
            sum = 0
            for item in y[window:i+1]:
                sum = sum + item
            moving_average_array.append(sum/len(y[window:i+1]))
            #print(moving_average_array[-1])
        i+=1
    #print("moving average list:", moving_average_array)
    return moving_average_array
    pass

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    diff = 0
    sum = 0
    for i in range(len(y)):
        diff = (y[i]-estimated[i])**2
        sum = sum + diff

    return ((sum/len(y))**0.5)


    pass

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual
        city temperatures for the given cities in a given year.
    """
    # TODO
    nat_yearly_temp =[]
    xval_year = []
    lastday=0
    for year in years:
        daily_avg_all_cities =[]
        for month in range(1,13):
            if month in [4,6,9,11]:
                #print( "this month for 30days")
                lastday = 30
            elif month == 2:
                if (((year % 4 == 0) and (year % 100 != 0)) or (year % 400 ==0)):
                    lastday = 29
                else:
                    lastday = 28
            else:
                lastday = 31
            for day in range(1,lastday+1):
                avg_temp_nat_day = []
                for city in multi_cities:
                    #print("city:", city, "year:", year, "month:", month, "day:", day)
                    avg_temp_nat_day.append(climate.get_daily_temp(city, month, day, year))
                daily_avg_all_cities.append(pylab.array(avg_temp_nat_day).mean())
        #print("year", year, " std dev: ", pylab.array(daily_avg_all_cities).std())
        nat_yearly_temp.append(pylab.array(daily_avg_all_cities).std())
        #print (year, ": ", len(avg_temp_nat_year))
        #print("year", year, " std dev: ", nat_yearly_temp)
    #print (len(nat_yearly_temp))
    return pylab.array(nat_yearly_temp)


    pass

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    #pylab.plot(x,y,"ob", label = "data")
    for i in range (len(models)):
        y_estimate = pylab.polyval(models[i], x)
        RSME = rmse(y, y_estimate)
        """if model is degree one or len of 2, se slope to be calculated"""
        """
        if len(models[i]==2):
            se = se_over_slope(x, y, y_estimate, models[i])
            pylab.plot(x,y_estimate,"-r", label = "model " + str(i) + " RMSE: " + str(round(RSME,5)) + " se slope: " + str(round(se,5)))
        if other than 1 degre model, plot the curve without se slope
        else:
        """
        pylab.plot(x,y,"ob", label = "data")
        pylab.plot(x,y_estimate,"-r", label = "model " + str(i) + " RMSE: " + str(round(RSME,5)))
        pylab.xlabel("Year")
        pylab.ylabel("maximum temperature in Celsius")
        pylab.legend(loc ='best')
        pylab.title("average temperature over the years")
        pylab.show()
    pass

if __name__ == '__main__':

    pass

    # Part A.4
    # TODO: replace this line with your code
    climate_data = Climate("data.csv")
    city_data = climate_data.rawdata
    temperature = []
    xval=[]
    #print(city_data.keys())
    for year in TRAINING_INTERVAL:
        temperature.append(city_data['NEW YORK'][year][1][10])
        xval.append(year)
        #print ('year:', year, 'temperature:', city_data['NEW YORK'][year][1][10] )
    xval=pylab.array(xval)
    yval = pylab.array(temperature)
    NY_model = generate_models(xval,yval,[1])
    #evaluate_models_on_training (xval,yval,NY_model)
    city = "NEW YORK"
    i=0
    yearly_temp =[]
    xval_year = []
    for year in TRAINING_INTERVAL:
        yearly_temp.append(climate_data.get_yearly_temp(city, year).mean())
        xval_year.append(year)
        #print (year,":",yearly_temp[i])
        #print(yearly_temp)
        #i+=1
    xval = pylab.array(xval_year)
    yval = pylab.array(yearly_temp)
    yearly_NY_model = generate_models(xval,yval,[1])
    #evaluate_models_on_training (xval,yval,yearly_NY_model)
    #print (temperature)
    # Part B
    # TODO: replace this line with your code
    national_yearly_temp = []
    national_yearly_temp = gen_cities_avg(climate_data, CITIES, TRAINING_INTERVAL)
    #xval = pylab.array(xval_year)
    yval = pylab.array(national_yearly_temp)
    yearly_national_model = generate_models(xval,yval,[1])

    #evaluate_models_on_training (xval,yval,yearly_national_model)
    # Part C
    # TODO: replace this line with your code
    yval_moving_average = pylab.array(moving_average(yval, 5))
    yearly_national_model_moving_avg = generate_models(xval,yval_moving_average,[1])
    #evaluate_models_on_training (xval,yval_moving_average,yearly_national_model_moving_avg)
    # Part D.2
    # TODO: replace this line with your code
    yval_moving_average = pylab.array(moving_average(yval, 5))
    yearly_national_model_moving_avg = generate_models(xval,yval_moving_average,[1,2,20])
    #print (yearly_national_model_moving_avg)
    #evaluate_models_on_training (xval,yval_moving_average,yearly_national_model_moving_avg)
    """ predict the result on TESTING_INTERVAL"""
    test_xval_year = []
    test_yearly_temp = []
    test_yearly_temp = gen_cities_avg(climate_data, CITIES, TESTING_INTERVAL)
    yval_test_moving_average = pylab.array(moving_average(test_yearly_temp,5))
    for year in TESTING_INTERVAL:
        test_xval_year.append(year)
    xval = pylab.array(test_xval_year)
    #print (xval, yval_test_moving_average)
    #yval = pylab.array(test_yearly_temp)

    #evaluate_models_on_testing (xval,yval_test_moving_average,yearly_national_model_moving_avg)


    # Part E
    # TODO: replace this line with your code
    std_dev_nat = gen_std_devs(climate_data, CITIES, TRAINING_INTERVAL)
    yval_std_dev_net = pylab.array(moving_average(std_dev_nat,5))
    #print(yval_std_dev_net)
    test_xval_year =[]
    for year in TRAINING_INTERVAL:
        test_xval_year.append(year)
    xval = pylab.array(test_xval_year)
    #print (len(xval), len(yval_std_dev_net), len(std_dev_nat))
    model_std_dev_moving_avg = generate_models(xval,yval_std_dev_net,[1])
    evaluate_models_on_training (xval,yval_std_dev_net,model_std_dev_moving_avg)
