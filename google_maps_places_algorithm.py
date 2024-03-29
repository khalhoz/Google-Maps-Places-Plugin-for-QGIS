# -*- coding: utf-8 -*-

"""
/***************************************************************************
 GoogleMapsPlaces
                                 A QGIS plugin
 This is a plugin to retrieve Places from Google using methods from the Places API.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-12-11
        copyright            : (C) 2023 by Alexandros Voukenas
        email                : avoukenas@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Alexandros Voukenas'
__date__ = '2023-12-11'
__copyright__ = '(C) 2023 by Alexandros Voukenas'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterString,
                       QgsProcessingParameterEnum,
                       QgsGeometry,
                       QgsPointXY,
                       QgsFields,
                       QgsField,
                       QgsFeature)
from qgis import processing
import googlemaps
import os 
import inspect

class GoogleMapsPlacesAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT_POINTS = 'INPUT POINTS'
    INPUT_KEY = 'API KEY'
    INPUT_RADIUS = "RADIUS"
    INPUT_TYPES = "TYPES"
    OUTPUT = 'OUTPUT'
    OPTIONS = ["airport",
               "amusement_park",
               "bank",
               "bar",
               "bus_station",
               "cafe",
               "cemetery",
               "church",
               "city_hall",
               "courthouse",
               "embassy",
               "fire_station",
               "gas_station",
               "hospital",
               "library",
               "light_rail_station",
               "local_government_office",
               "mosque",
               "movie_theater",
               "museum",
               "park",
               "parking",
               "police",
               "post_office",
               "primary_school",
               "restaurant",
               "school",
               "secondary_school",
               "shopping_mall",
               "stadium",
               "supermarket",
               "synagogue",
               "train_station",
               "university",
               "zoo"
               ]

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return GoogleMapsPlacesAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'downloadgooglemapsplaces'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Download Google Maps Places')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('')
        
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'download_places_logo.png')))
        return icon

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("This algorithm is used to download Google Maps Places around sample point locations and a specific radius. \n The user defines the sample points dataset, the types of places to download (bar, cafe, restaurant, etc.) and a search radius. The algorithm will look for and download the Places from Google Maps with the specified Types and within the specified radius of the sample points. An API key is also required from the Google Maps Platform. See the documentation on how to obtain an API key. \n The Input sample points layer must be in WGS84 Geographic Reference System (epsg:4326) and the search radius must be in meters.")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_POINTS,
                self.tr('Input sample points layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_RADIUS,
                self.tr('Search Radius in meters'),
                defaultValue=''
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(self.INPUT_TYPES, self.tr('Types of Places to download'), options=self.OPTIONS,
                                       allowMultiple=True, usesStaticStrings=False, defaultValue=[]))

        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_KEY,
                self.tr('Google Maps Places API key'),
                defaultValue=''
            )
        )
        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Google Maps Places')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        
        source = self.parameterAsSource(parameters, self.INPUT_POINTS, context)
        #Check if the source is in the right crs
        if source.sourceCrs().authid()!='EPSG:4326':
            raise QgsProcessingException(self.tr('Coordinate Reference System of Input layer must be WGS84 Geographic (epsg:4326)'))
            
        radius = self.parameterAsString(parameters, self.INPUT_RADIUS, context)
        types_list = self.parameterAsEnums(parameters, self.INPUT_TYPES, context)
        api_key = self.parameterAsString(parameters, self.INPUT_KEY, context)
        
        #create fields for the output layer
        fields = QgsFields()
        fields.append(QgsField("type", QVariant.String))
        fields.append(QgsField("name", QVariant.String))
        fields.append(QgsField("place_id", QVariant.String))
        
        #create the output sink
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context, fields, 4, source.sourceCrs())
        
        #initiate a google maps API call
        gmaps = googlemaps.Client(api_key)
        
        #get the features of the input into an iteratable
        it = source.getFeatures()
        places_ids=[]
        
        #loop through the features of the input layer. For each feature,
        #perform an API call based on the defined parameters.
        #This is done by retrieving the coordinates of each point first
        #Also, each time a Place is found, it's place_id is appended on the places_ids list
        #This way, if the same point is found twice, it won't be written again on the output
        for feature in it:
            geom = feature.geometry()
            long = geom.asPoint()[0]
            lat = geom.asPoint()[1]
            
            for ltype in types_list:
                
                keyword = self.OPTIONS[ltype]
                result = gmaps.places_nearby('{},{}'.format(lat, long), radius=radius, type=keyword)
                for request_result in result['results']:
                    location = request_result['geometry']['location']
                    name = request_result['name']
                    place_id=request_result['place_id']
                    if place_id not in places_ids:
                        lat = round(location['lat'], 4)
                        lng = round(location['lng'], 4)

                        point = QgsPointXY(lng, lat)
                        geometry = QgsGeometry.fromPointXY(point)
                        new_feature = QgsFeature()
                        new_feature.setGeometry(geometry)
                        new_feature.setAttributes([keyword, name,place_id])

                        sink.addFeature(new_feature, QgsFeatureSink.FastInsert)
                    places_ids.append(place_id)

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}